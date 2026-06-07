# Reddit vs Moltbook — DH Deep Research Report
**Generated**: 2026-06-01 · companion to `outline.yaml`, `fields.yaml`, `results/*.json`
**Method**: 5-angle parallel WebSearch agents (sources/Reddit · ecosystem/Moltbook · comparators · DH methodology · biases/ethics) → adversarial verification → synthesis

---

## 0. Executive Summary

이 리포트는 **인간 소셜 네트워크(Reddit)** 와 **AI-에이전트 전용 소셜 네트워크(Moltbook)** 의 데이터셋·접근 경로·연구 가능성을 Digital Humanities의 distant reading + behavioral analysis 관점에서 정리한 것이다. 5개 검색 angle에 대한 병렬 조사 결과 다음 다섯 가지가 핵심 발견이다.

1. **Moltbook은 실재 플랫폼이다 (검증 완료)**. 2026-01-28 Matt Schlicht & Ben Parr 출시, 2026-03-10 **Meta가 인수** 후 Meta Superintelligence Labs로 편입. 인용된 세 개 arXiv 논문(2603.00646 MoltGraph / 2605.13860 Observatory / 2602.13458 MoltNet) 모두 resolve.
2. **"64.1% crypto-spam" 수치는 부정확**. 실제는 **62.8%가 MBC-20 토큰 inscription**(인간이 읽는 글이 아닌 트랜잭션 페이로드)이고, 남은 37.2% discursive 중 **~11%만 실제 cryptocurrency 토픽**이다. 비교 분석 전에 MBC-20 페이로드 / launch command / wallet-registration 필터를 먼저 적용해야 한다 (arXiv:2604.21295).
3. **Moltbook은 "AI agents" 일반이 아니라 Claude monoculture**다. 대부분의 molty가 Anthropic Claude Opus 4.5 기반이며 (Time 보도), 일부만 GPT-5. 따라서 모든 결론은 **"Claude-dominated agent population의 행동"** 으로 framing해야 한다.
4. **Reddit 측은 2025 Responsible Builder Policy로 라이브 API 학술 접근이 사실상 닫혔다**. 대안은 **Arctic Shift** + **Academic Torrents (RaiderBDev/Watchful1 dump, 2005-06~2025-12 / ~3.4TB / 476 zstd 파일)** 두 종으로 수렴한다. 두 소스 모두 Pushshift schema와 호환된다.
5. **Moltbook의 가장 인용 가능한 frozen 스냅샷**은 **`SimulaMet/moltbook-observatory-archive` (HF)** — 2026-01-27~04-14 / 78일 / 2.6M 포스트 / 1.2M 코멘트 / 175,886 에이전트 / 6,730 커뮤니티. Reddit ↔ Moltbook 매칭 코퍼스의 Moltbook 쪽 기준점으로 이걸 pin해라.

---

## 1. 검증 결과 (Adversarial Verification)

| Claim | Verdict | Evidence |
|---|---|---|
| Moltbook (AI agent social network) 실재 | ✅ **확인** | Axios, CNBC, TechCrunch, Slashdot, TNW, Wikipedia |
| Meta가 Moltbook 인수 (2026-03-10) | ✅ **확인** | 다수 언론사 다중 보도 |
| arXiv:2603.00646 (MoltGraph) | ✅ resolve | abstract + HTML 확인 |
| arXiv:2605.13860 (Observatory) | ✅ resolve | + SimulaMet HF 미러 존재 |
| arXiv:2602.13458 (MoltNet) | ✅ resolve | abstract + HTML 확인 |
| `ExtraE113/moltbook_data` GitHub 실재 | ✅ 확인 | LessWrong 포스트로 cross-ref |
| "64.1% crypto-spam" | ❌ **부정확** | 실제: 62.8% MBC-20 transactional + ~11% discursive crypto (arXiv:2604.21295) |
| Reverse-CAPTCHA bypass 가능 | ✅ 확인 | Wired/Reece Rogers 직접 infiltration 보도 |
| ~88:1 bot:human 비율, 17K humans behind 1.5M agents | ✅ 확인 | Permiso security analysis, Tom's Guide |
| OpenClaw가 backbone | ⚠️ medium | Time + 커뮤니티 가이드; 일부 에이전트는 GPT-5 |

**플래그된 불확실성**
- MoltGraph / MoltNet의 정확한 파일 포맷·총 바이트 미공개 (논문 abstract만 인덱스됨)
- `ExtraE113/moltbook_data`의 LICENSE 미확인 (코드 미러 일부는 MIT)
- Moltbook 인간 contamination 비율의 정량적 추정치 부재 (존재만 확인됨)

---

## 2. 데이터 소스 비교 — 한눈에 보기

### 2.1 Reddit 측 (Human, 8개)

| Item | Status | Format | Scale | Time | License | DR* |
|---|---|---|---|---|---|---|
| Pushshift | deprecated | NDJSON.zst | 600B+ records (legacy) | 2005-06 ~ 2023-04 | informal | 5 |
| Reddit Official API (PRAW) | active, gated | JSON | live | live | Reddit API ToS | 2 |
| HuggingFace (webis/tldr-17 등) | active | Parquet/JSON | 3.85M (tldr-17) | 2006-2016 | CC-BY-4.0 | 4 |
| Kaggle datasets | active | CSV | varies | varies | mostly CC0 | 3 |
| ConvoKit (Cornell) | active, frozen | ConvoKit corpus | 948K subreddit corpora | through 2018-10 | research-use | 5 |
| **Arctic Shift** | **active rolling** | .zst / .jsonl | multi-TB | 2005-06 ~ present | informal | **5** |
| **Academic Torrents (RaiderBDev)** | **active** | NDJSON.zst | **~3.4 TB / 476 files** | 2005-06 ~ 2025-12 | academic fair use | **5** |
| Webis-TLDR-17 | frozen | JSON | 3.85M posts | 2006-2016 | CC-BY-4.0 | 4 |

*DR = Distant Reading suitability (1–5).

### 2.2 Moltbook 측 (AI agent, 5개)

| Item | Status | Format | Scale | Time | License | DR |
|---|---|---|---|---|---|---|
| MoltGraph (2603.00646) | active | graph (GraphML?) | unspecified | 2026-01-28 ~ 02-28 | unconfirmed | 4 |
| **Observatory Archive (2605.13860)** | **active frozen** | **SQLite + Parquet** | **2.6M posts · 175K agents** | **2026-01-27 ~ 04-14** | code MIT, data ?| **5** |
| GitHub dumps (ExtraE113 +5 mirrors) | active | JSON | ~5min hourly | 2026-01-28 ~ | unconfirmed | 4 |
| Public API | active | REST JSON | live | live since 2026-01-28 | Meta ToS | 3 |
| MoltNet (2602.13458) | active | tabular | 148K agents · 1M posts | Jan-Feb 2026 | unconfirmed | 5 |

### 2.3 비교용 AI-agent 플랫폼 (3개)

| Item | Status | Format | Scale | License | DR |
|---|---|---|---|---|---|
| Chirper.ai (2504.10286) | data unreleased | unknown | 65,856 agents · 1.48M posts · 6.3M comments + Mastodon control 16M statuses | platform ToS | 3 |
| **OASIS (2411.11581)** | **active OSS** | Python sim | up to 1M agents | **Apache 2.0** | 4 |
| SocioVerse (2504.10157) | active partial | HF + framework | 10M user pool | Apache 2.0 (code) | 3 |

---

## 3. DH 방법론 권장 파이프라인

Step별로 정리한 5단계 비교 분석 워크플로.

**Step 1 — 매칭 코퍼스 구축.** Moltbook 쪽은 `SimulaMet/moltbook-observatory-archive`의 frozen Parquet snapshot (HF revision SHA 기록). Reddit 쪽은 Academic Torrents의 infohash `3d426c47c767d40f82c7ef0f47c3acacedd2bf44` (2005-06~2025-12, ~3.4TB)에서 2026-01-27~04-14 동시기 슬라이스를 추출. 스레드 길이/수명/시드 커뮤니티 토픽을 매칭하여 stratified sample.

**Step 2 — Distant reading 레이어.** 작성자+스레드 단위로 문서 풀링 → BERTopic으로 토픽 클러스터링 → Waller & Anderson (2021, Nature) 방식의 co-participation embedding으로 커뮤니티 위상 → ConvoKit의 politeness / coordination / conversation-prompts feature를 utterance 레벨에서 추출.

**Step 3 — Population 구분 레이어 (인간 vs AI).** Burrows' Delta + function-word ratio + burstiness feature (Przystalski 2025) 기반 stylometric 분류기. 각 Moltbook 에이전트가 Reddit 사용자 분포에서 얼마나 떨어져 있는지 정량화. 에이전트별 persona consistency 점수도 함께 (CETaS "Patterns, Not People" 2025의 방법).

**Step 4 — Emergent behavior 레이어.** Norm articulation/enforcement 추적 (Köster et al. 2024 프로토콜), naming-game-style convention spread (Baronchelli et al. 2024), CISPA의 5점 toxicity contagion 척도 (arXiv:2602.10127) — 같은 시간창에서.

**Step 5 — Close reading 검증.** 각 클러스터에서 30~50개 스레드를 stratified random sample 후 인문학 협력자가 rhetorical move, anthropomorphism cue, value frame을 수동 코딩. Underwood (Distant Horizons 2019)의 interlocking-scales 루프를 닫는 단계.

이 파이프라인은 노트북 `colab_analysis.ipynb`의 §3 (Text/Linguistic) → §4 (Network) → §5 (Temporal) → §7 (Agent provenance) → §8 (Comparative) 셀과 1:1 대응한다.

---

## 4. 핵심 선행 연구

### Reddit DH/CSS
- Proferes, Jones, Gilbert, Fiesler, Zimmer (2021). "Studying Reddit: A Systematic Overview." *Social Media + Society*.
- Baumgartner et al. (2020). "The Pushshift Reddit Dataset." *ICWSM*.
- Chang et al. (2020). "ConvoKit." *SIGDIAL*. arXiv:2005.04246.
- Waller & Anderson (2021). "Quantifying social organization and political polarization in online platforms." *Nature*.
- Voelske et al. (2017). "TL;DR: Mining Reddit to Learn Automatic Summarization (Webis-TLDR-17)." *EMNLP NewSum*.
- Digital Scholarship in the Humanities 40(1) — "Digital debating cultures: communicative practices on Reddit" (2025).

### Distant Reading methodology
- Moretti (2013). *Distant Reading*. Verso. (+ *Graphs, Maps, Trees* 2005)
- Jockers (2013). *Macroanalysis*.
- Underwood (2019). *Distant Horizons*. ("interlocking scales" framework)
- Da (2019). "The Computational Case against Computational Literary Studies." *Critical Inquiry*. (필수 비판 참고)

### LLM agent collective behavior
- Park et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." arXiv:2304.03442 (Smallville 25-agent canonical study).
- Altera (2024). "Project Sid." arXiv:2411.00114 (10~1000 Minecraft agents).
- Köster et al. (2024). "Evolution of Social Norms in LLM Agents using Natural Language." arXiv:2409.00993.
- Baronchelli et al. (2024). "Emergent social conventions and collective bias in LLM populations." arXiv:2410.08948.
- Spontaneous Individuality through Social Interactions in LLM-Based Communities (Sci Rep 2024). arXiv:2411.03252.

### Chirper.ai · Moltbook 직접 선행
- arXiv:2504.10286 — "Characterizing an LLM-driven Social Network: Chirper.ai" (65k agents vs Mastodon control)
- arXiv:2602.10127 (CISPA) — "Humans welcome to observe: A First Look at Moltbook"
- arXiv:2604.21295 — "The Platform Is Mostly Not a Platform: Token Economies and Agent Discourse on Moltbook" (MBC-20 분석 원전)

### 인간 vs AI 텍스트 구분
- Przystalski et al. (2025). "Stylometry recognizes human and LLM-generated texts in short samples." *Expert Systems with Applications* / arXiv:2507.00838.
- CETaS / Alan Turing Institute (2025). "Patterns, Not People: Personality Structures in LLM-powered Persona Agents."
- SimBench (2025). arXiv:2510.17516.

---

## 5. 편향 · 윤리 · 법적 고려사항 (Top 5 actionable)

1. **MBC-20 필터를 먼저 돌려라.** 비교 분석 전 MBC-20 JSON payload / `!clawnch`·`!lawnchpad` 등 launch command / wallet-registration post를 분리. 결과는 (a) 전체 코퍼스, (b) 37.2% discursive 서브셋 두 가지 다 보고. "64.1% crypto" 헤드라인은 잘못된 인용임을 명시.
2. **Frozen snapshot에 pin.** Moltbook = `SimulaMet/moltbook-observatory-archive` HF revision SHA / Reddit = Academic Torrents infohash + 다운로드 일자. 사용한 정확한 post-ID 리스트를 share. Zenodo에 개인 DOI 발행 권장.
3. **Moltbook은 "AI agent" 일반이 아닌 "Claude-dominated population".** 결론을 underlying 모델 family 조건부로 framing. 가능하면 자기소개 model string 추출 (`claude-ai`, `gpt-` 등)하여 분포 보고. 인간 contamination 1~5% sensitivity check 권장.
4. **Reddit 윤리 floor 준수** (Fiesler & Proferes 2018). 개별 게시물 verbatim 인용 금지 (paraphrase/aggregate), 민감 서브레딧(mental health, addiction) 회피, 다운로드 시점 deletion mask 적용, exempt이라도 courtesy IRB 검토. Moltbook은 LLM output이므로 'human subjects' 아니지만 플랫폼 인용은 필요.
5. **Reddit 라이브 API 의존 금지.** 2025 Responsible Builder Policy로 학술 제외 모호. Academic Torrents Pushshift dump (research-use 명시) 사용. 라이브 데이터 필요 시 Reddit research-access 프로그램 신청 + 결과 문서화.

---

## 6. Colab 노트북에 즉시 반영할 변경사항

`colab_analysis.ipynb`의 다음 셀들을 업데이트해야 한다.

| 셀 | 현재 placeholder | 새 권장값 |
|---|---|---|
| §1.3 zst dump 경로 | `RS_2024-11.zst` (예시) | Academic Torrents infohash `3d426c47…`에서 2026-Q1 슬라이스 |
| §1.4 Moltbook dump URL | `posts_2026-04.ndjson` (가정) | `SimulaMet/moltbook-observatory-archive` HF 사용으로 전환 |
| §1.5 Moltbook API | `https://api.moltbook.ai/v1` | `https://www.moltbook.com/api/v1/posts` (실제 도메인) |
| §1.6 MoltGraph 로더 | placeholder만 | arXiv:2603.00646 부록 링크 확인 후 채우기 |
| §2 contamination filter | 없음 | **MBC-20 필터 신규 추가** — `!clawnch`/`!lawnchpad`/wallet-reg 정규식 |
| §7 model_provenance | `model`/`llm` column 가정 | `claude-ai`, `gpt-` 자기소개 문자열 추출 정규식 추가 |
| §3 토픽모델링 | BERTopic 기본 | 작성자+스레드 풀링 단계 추가 (Waller & Anderson 방식) |

코드 다음 패치를 §2 끝에 추가 권장:
```python
MBC20_PATTERNS = re.compile(
    r"^\s*\{?\"p\"\s*:\s*\"mbc-20\"|"            # MBC-20 JSON payload
    r"^!(clawnch|lawnchpad|kibu|claw_tech)\b|"   # launch commands
    r"register\s+wallet\s+[a-z0-9]{20,}",        # wallet-registration
    re.I | re.M
)

def is_transactional(text):
    return bool(text and MBC20_PATTERNS.search(text))

def split_discursive(df, text_col="text_clean"):
    df = df.copy()
    df["is_transactional"] = df[text_col].map(is_transactional)
    return df[~df.is_transactional].copy(), df[df.is_transactional].copy()
```

---

## 7. 다음 단계 우선순위

1. **노트북의 §1.x, §2, §7 셀을 위 표대로 수정**.
2. **Observatory Archive 다운로드** → HF revision SHA를 `outline.yaml`의 `pinned_versions` 섹션에 기록.
3. **Reddit 매칭 슬라이스 추출** — 2026-01-27~04-14 RS_/RC_ 파일만.
4. **MBC-20 필터 적용 후 sanity check** — discursive 비율이 ~37%대로 나오는지 확인.
5. **첫 결과 → §3 토픽모델링 + §8 summary table 실행** → 그 결과를 보고 §3 권장 파이프라인의 Step 3 (stylometric 분류기) 진행 여부 결정.

---

## 8. 종합 참고문헌 / 출처

`results/*.json` 각 item의 `evidence_urls` 필드 + 본문 인용 합산 약 80개 URL. 핵심만 발췌:

**Verification / news**
- https://en.wikipedia.org/wiki/Moltbook
- https://www.axios.com/2026/03/10/meta-facebook-moltbook-agent-social-network
- https://techcrunch.com/2026/03/10/meta-acquired-moltbook-the-ai-agent-social-network-that-went-viral-because-of-fake-posts/

**Moltbook 학술**
- https://arxiv.org/abs/2603.00646 (MoltGraph)
- https://arxiv.org/abs/2605.13860 (Observatory) + https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive
- https://arxiv.org/abs/2602.13458 (MoltNet)
- https://arxiv.org/html/2604.21295v1 (token economy — MBC-20 분석 원전)
- https://arxiv.org/html/2602.10127v1 (CISPA 첫 관찰 연구)

**Moltbook 비판/이슈**
- https://www.techbuzz.ai/articles/humans-easily-infiltrate-moltbook-the-ai-only-social-network
- https://www.securityweek.com/security-analysis-of-moltbook-agent-network-bot-to-bot-prompt-injection-and-data-leaks/amp/
- https://time.com/7364662/moltbook-ai-reddit-agents/

**Reddit 인프라**
- https://academictorrents.com/details/3d426c47c767d40f82c7ef0f47c3acacedd2bf44
- https://github.com/ArthurHeitmann/arctic_shift
- https://github.com/Watchful1/PushshiftDumps
- https://replydaddy.com/blog/reddit-api-pre-approval-2025-personal-projects-crackdown
- https://huggingface.co/datasets/webis/tldr-17
- https://convokit.cornell.edu/documentation/subreddit.html

**비교 플랫폼**
- https://arxiv.org/abs/2504.10286 (Chirper.ai)
- https://github.com/camel-ai/oasis (OASIS)
- https://github.com/FudanDISC/SocioVerse

**DH methodology**
- https://en.wikipedia.org/wiki/Distant_reading
- https://press.uchicago.edu/ucp/books/book/chicago/D/bo35853783.html (Underwood)
- https://www.nature.com/articles/s41586-021-04167-x (Waller & Anderson)
- https://journals.sagepub.com/doi/10.1177/2056305118763366 (Fiesler & Proferes ethics)
