"""
슬라이드용 데이터 CSV 내보내기.

사용법: 노트북에서 §1~§8 분석 셀을 모두 실행해 아래 변수들이 메모리에 있는 상태에서,
        이 파일 내용을 노트북 마지막 셀에 붙여 실행한다(또는 %load scripts/export_results.py).

필요한 in-memory 변수:
  df_canon (피처 포함: n_tokens, ttr, first_person_rate, compound_sent, mtld, n_replies, score,
            created_utc, platform, author_id, community, parent_id, post_id)
  df_reddit, df_reddit_c, df_moltbook, df_moltbook_c, df_agents
  G_reddit, G_molt                       (§4 reply 그래프)
  to_canonical_reddit, to_canonical_moltbook, infer_model_from_text  (노트북 정의 함수)

출력: <repo>/presentation/data/*.csv  (UTF-8-SIG, 엑셀에서도 한글 OK)
"""
import numpy as np, pandas as pd

OUT = PROJECT.parent / "presentation" / "data"          # PROJECT = 노트북 §0에서 정의됨
OUT.mkdir(parents=True, exist_ok=True)

def save(df, name):
    p = OUT / name
    df.to_csv(p, index=False, encoding="utf-8-sig")
    print("✓", name, tuple(df.shape))

# 1) 요약표 ------------------------------------------------------------------
rows = []
for p, g in df_canon.groupby("platform"):
    rows.append(dict(platform=p, n_posts=len(g), n_authors=g.author_id.nunique(),
        posts_per_author=round(len(g)/g.author_id.nunique(), 3),
        median_tokens=g["n_tokens"].median() if "n_tokens" in g else np.nan,
        median_mtld=g["mtld"].median() if "mtld" in g else np.nan,
        mean_first_person=g["first_person_rate"].mean() if "first_person_rate" in g else np.nan,
        mean_sentiment=g["compound_sent"].mean() if "compound_sent" in g else np.nan,
        mean_replies=g["n_replies"].mean(), median_score=g["score"].median()))
save(pd.DataFrame(rows), "summary.csv")

# 2) 피처 분포 히스토그램(tidy: feature, platform, bin_center, share) --------
def hist_tidy(df, col, feature, bins=30, log=False):
    out = []
    # 공통 빈 경계: 두 플랫폼 전체 값으로 edges를 한 번만 계산한다.
    # (이전 버전은 플랫폼마다 따로 np.histogram을 호출해 빈 폭이 달라졌고,
    #  y축이 share라서 빈 폭이 넓은 쪽의 면적이 부당하게 커 보이는 문제가 있었음)
    v_all = df[col].dropna().values
    if log: v_all = np.log1p(v_all)
    if len(v_all) == 0: return pd.DataFrame(out)
    edges = np.histogram_bin_edges(v_all, bins=bins)
    ctr = (edges[:-1] + edges[1:]) / 2
    for p, g in df.groupby("platform"):
        v = g[col].dropna().values
        if log: v = np.log1p(v)
        if len(v) == 0: continue
        cnt, _ = np.histogram(v, bins=edges)   # 공통 edges 사용 → 빈 폭 통일
        sh = cnt / cnt.sum()
        for c, s in zip(ctr, sh):
            out.append(dict(feature=feature, platform=p, bin_center=round(float(c), 4), share=round(float(s), 5)))
    return pd.DataFrame(out)

feat = []
if "n_tokens" in df_canon:          feat.append(hist_tidy(df_canon, "n_tokens", "log_n_tokens", log=True))
if "ttr" in df_canon:               feat.append(hist_tidy(df_canon, "ttr", "ttr"))
if "first_person_rate" in df_canon: feat.append(hist_tidy(df_canon, "first_person_rate", "first_person_rate"))
if "compound_sent" in df_canon:     feat.append(hist_tidy(df_canon, "compound_sent", "sentiment"))
if "mtld" in df_canon:              feat.append(hist_tidy(df_canon.dropna(subset=["mtld"]), "mtld", "mtld"))
if feat: save(pd.concat(feat, ignore_index=True), "feature_hist.csv")

# 3) circadian (시간대별 share) + 통계 --------------------------------------
tmp = df_canon.copy()
tmp["hour"] = pd.to_datetime(tmp["created_utc"], utc=True).dt.hour
piv = tmp.groupby(["platform", "hour"]).size().rename("n").reset_index()
piv["share"] = piv.groupby("platform")["n"].transform(lambda s: s / s.sum())
save(piv[["platform", "hour", "share"]], "circadian.csv")
crows = []
for p, g in piv.groupby("platform"):
    s = g.set_index("hour")["share"]
    crows.append(dict(platform=p, cv=round(s.std()/s.mean(), 3),
        peak_hour=int(s.idxmax()), peak_share=round(float(s.max()), 4),
        trough_hour=int(s.idxmin()), trough_share=round(float(s.min()), 4)))
save(pd.DataFrame(crows), "circadian_stats.csv")

# 4) 작성자 활동(글+댓글) ----------------------------------------------------
try:
    contrib = pd.concat([to_canonical_reddit(df_reddit), to_canonical_reddit(df_reddit_c),
                         to_canonical_moltbook(df_moltbook), to_canonical_moltbook(df_moltbook_c)],
                        ignore_index=True)
    cnt = contrib.groupby(["platform", "author_id"]).size().rename("c").reset_index()
    asum = cnt.groupby("platform").agg(n_authors=("author_id", "nunique"), total=("c", "sum")).reset_index()
    asum["per_author"] = round(asum["total"] / asum["n_authors"], 3)
    save(asum, "author_summary.csv")
    ha = []
    for p, g in cnt.groupby("platform"):
        v = np.log1p(g["c"].values); c2, e = np.histogram(v, bins=30); sh = c2 / c2.sum()
        ctr = (e[:-1] + e[1:]) / 2
        for cc, ss in zip(ctr, sh):
            ha.append(dict(platform=p, log_bin_center=round(float(cc), 4), share=round(float(ss), 5)))
    save(pd.DataFrame(ha), "author_activity_hist.csv")
except NameError as e:
    print("· author activity 스킵 (댓글 df 필요):", e)

# 5) reply 깊이 분포 ---------------------------------------------------------
try:
    import networkx as nx
    def depth_share(G):
        lvl = {}
        for d, gen in enumerate(nx.topological_generations(G)):
            for n in gen: lvl[n] = d
        s = pd.Series(lvl); s = s[s >= 1].clip(upper=5)
        return s.value_counts(normalize=True).sort_index()
    dd = []
    for name, G in [("reddit", G_reddit), ("moltbook", G_molt)]:
        for d, sh in depth_share(G).items():
            dd.append(dict(platform=name, depth=f"{int(d)}{'+' if d == 5 else ''}", share=round(float(sh), 5)))
    save(pd.DataFrame(dd), "reply_depth.csv")
except NameError as e:
    print("· reply depth 스킵 (G_reddit/G_molt 필요):", e)

# 6) 글당 답글 수 / 주목 집중도 ----------------------------------------------
rr = []
for p, g in df_canon.groupby("platform"):
    d = g["n_replies"].dropna().sort_values(ascending=False).values
    tot = d.sum() or 1
    rr.append(dict(platform=p, n_posts=len(d), mean=round(float(d.mean()), 3),
        median=float(np.median(d)), max=int(d.max()),
        top1pct_share=round(float(d[:max(1, len(d)//100)].sum()/tot), 4)))
save(pd.DataFrame(rr), "replies_per_post.csv")

# 7) 모델 provenance ---------------------------------------------------------
try:
    pv = []
    for m, c in df_moltbook["content"].fillna("").map(infer_model_from_text).dropna().value_counts().items():
        pv.append(dict(source="post_content", model=m, count=int(c)))
    for m, c in df_agents["description"].fillna("").map(infer_model_from_text).dropna().value_counts().items():
        pv.append(dict(source="agent_bio", model=m, count=int(c)))
    save(pd.DataFrame(pv), "provenance.csv")
except NameError as e:
    print("· provenance 스킵 (df_agents/infer_model_from_text 필요):", e)

# 8) 분포 차이 검정 ----------------------------------------------------------
try:
    from scipy import stats
    st = []
    for col in ["n_tokens", "ttr", "first_person_rate", "compound_sent", "mtld", "n_replies"]:
        if col not in df_canon: continue
        a = df_canon.loc[df_canon.platform == "reddit", col].dropna()
        b = df_canon.loc[df_canon.platform == "moltbook", col].dropna()
        if len(a) < 2 or len(b) < 2: continue
        ks = stats.ks_2samp(a, b); mw = stats.mannwhitneyu(a, b, alternative="two-sided")
        st.append(dict(feature=col, ks_stat=round(ks.statistic, 4), ks_p=ks.pvalue, mw_p=mw.pvalue,
            mean_reddit=round(float(a.mean()), 4), mean_moltbook=round(float(b.mean()), 4)))
    save(pd.DataFrame(st), "stat_tests.csv")
except Exception as e:
    print("· stat tests 스킵:", e)

print("\n완료 →", OUT)
