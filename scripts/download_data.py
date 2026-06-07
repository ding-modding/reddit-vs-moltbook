"""
DH-Project 데이터 다운로더 — §1.3 Reddit + §1.4 Moltbook.

이 환경(Claude 샌드박스)에서는 HF·Arctic Shift·Academic Torrents가 모두 막혀 있어
사용자 PC에서 직접 실행하도록 만든 스크립트다. 받은 데이터는 data/raw/ 에 저장된다.

사용:
    pip install -r requirements.txt
    python scripts/download_data.py                       # 기본: 매칭 최근 윈도우(2026-04-01~04-14)
    python scripts/download_data.py --launch              # 출시주(2026-01-27~)
    python scripts/download_data.py --after 2026-03-15 --before 2026-04-14
    python scripts/download_data.py --full                # Moltbook 전체(~2GB) / Reddit 윈도우 무제한
    python scripts/download_data.py --moltbook-only        # / --reddit-only

설계 메모:
  * Moltbook 아카이브는 frozen 스냅샷(2026-01-27~04-14)이라 그 이후 "최신"은 없다.
  * 기본 윈도우를 아카이브 후반(04-01~04-14)으로 잡아 출시주 편향(85%가 1/31)을 피한다.
  * Moltbook은 parquet shard를 끝에서부터 읽어 윈도우만 필터(전체 1.6GB 안 받아도 됨).
  * Reddit은 3.4TB 토렌트 대신 Arctic Shift HTTP API로 같은 윈도우만 받는다.
"""
from __future__ import annotations
import argparse, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
REDDIT_DIR = RAW / "reddit"
MOLT_DIR = RAW / "moltbook"

# ── 기본 설정 (필요하면 여기만 수정) ─────────────────────────────────────────
# 기본 = 아카이브 후반 매칭 윈도우 (안정기, 출시 편향 없음)
WINDOW_AFTER = "2026-04-01"
WINDOW_BEFORE = "2026-04-14"
# --launch 사용 시 이 윈도우로 대체
LAUNCH_AFTER, LAUNCH_BEFORE = "2026-01-27", "2026-02-03"

SUBREDDITS = [
    "artificial", "singularity", "LocalLLaMA",      # AI/기술
    "offmychest", "CasualConversation",             # 고백·일상
    "CryptoCurrency",                               # 크립토
    "ProgrammerHumor",                              # 유머
]

MOLTBOOK_REPO = "SimulaMet/moltbook-observatory-archive"
MOLTBOOK_CONFIGS = ["posts", "comments", "agents"]
MOLTBOOK_CONFIGS_FULL = ["posts", "comments", "agents",
                         "snapshots", "submolts", "word_frequency"]
# config별 시간 필터 컬럼
DATE_COL = {"posts": "created_at", "comments": "created_at", "agents": "last_seen_at",
            "snapshots": "created_at", "submolts": "created_at", "word_frequency": "created_at"}

REDDIT_SAMPLE_PER_SUB = 5_000   # --full 이면 무제한
MOLT_CAP_PER_CONFIG = 50_000

ARCTIC = "https://arctic-shift.photon-reddit.com/api"
# ─────────────────────────────────────────────────────────────────────────────


def _epoch(d: str) -> int:
    return int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


# ── §1.3 Reddit (Arctic Shift API) ──────────────────────────────────────────
def download_reddit(after: str, before: str, full: bool):
    import requests
    REDDIT_DIR.mkdir(parents=True, exist_ok=True)
    a0, b0 = _epoch(after), _epoch(before)
    cap = None if full else REDDIT_SAMPLE_PER_SUB
    sess = requests.Session()
    sess.headers["User-Agent"] = "DH-Project/1.0 (academic distant-reading)"

    for kind, ep in [("posts", "posts/search"), ("comments", "comments/search")]:
        for sub in SUBREDDITS:
            out = REDDIT_DIR / f"{sub}_{kind}.ndjson"
            n, after_cur = 0, a0
            print(f"[reddit] r/{sub} {kind} ({after}~{before}) → {out.name}")
            with out.open("w", encoding="utf-8") as fh:
                while True:
                    params = {"subreddit": sub, "after": after_cur, "before": b0,
                              "limit": 100, "sort": "asc"}
                    try:
                        r = sess.get(f"{ARCTIC}/{ep}", params=params, timeout=60)
                        r.raise_for_status()
                        rows = r.json().get("data", [])
                    except Exception as e:
                        print(f"   ! {sub}/{kind} 중단: {e}")
                        break
                    if not rows:
                        break
                    for row in rows:
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                    n += len(rows)
                    after_cur = int(rows[-1].get("created_utc", after_cur)) + 1
                    if cap and n >= cap:
                        print(f"   샘플 한도 {cap} 도달"); break
                    if len(rows) < 100:
                        break
                    time.sleep(0.5)
            print(f"   ✓ {n:,} rows")


# ── §1.4 Moltbook (HF Observatory Archive, parquet shard) ───────────────────
def download_moltbook(after: str, before: str, full: bool):
    import pandas as pd
    from huggingface_hub import HfApi, hf_hub_download
    MOLT_DIR.mkdir(parents=True, exist_ok=True)

    api = HfApi()
    sha = api.dataset_info(MOLTBOOK_REPO).sha
    _record_revision(sha, after, before, full)
    print(f"[moltbook] repo={MOLTBOOK_REPO}  revision={sha}")

    a = pd.Timestamp(after, tz="UTC")
    b = pd.Timestamp(before, tz="UTC")
    REV = "refs/convert/parquet"
    all_files = api.list_repo_files(MOLTBOOK_REPO, repo_type="dataset", revision=REV)

    configs = MOLTBOOK_CONFIGS_FULL if full else MOLTBOOK_CONFIGS
    for cfg in configs:
        out = MOLT_DIR / f"{cfg}.parquet"
        shards = sorted(f for f in all_files if f.startswith(f"{cfg}/") and f.endswith(".parquet"))
        if not shards:
            print(f"   ! {cfg}: parquet shard 없음 (스킵)"); continue
        col = DATE_COL.get(cfg, "created_at")
        print(f"[moltbook] {cfg} ({after}~{before}, {len(shards)} shards) → {out.name}")

        frames, got = [], 0
        # 아카이브는 시간순(앞=출시주) → 최근 윈도우는 끝에서부터 읽는 게 효율적
        for shard in reversed(shards):
            try:
                p = hf_hub_download(MOLTBOOK_REPO, shard, repo_type="dataset", revision=REV)
                raw = pd.read_parquet(p)          # shard는 한 번만 읽음
            except Exception as e:
                print(f"   ! shard {shard} 실패: {e}"); continue
            if full or col not in raw.columns:
                frames.append(raw); got += len(raw)
                if not full and got >= MOLT_CAP_PER_CONFIG:
                    break
                continue
            ts = pd.to_datetime(raw[col], utc=True)
            sub = raw[(ts >= a) & (ts < b)]
            if len(sub):
                frames.append(sub); got += len(sub)
            if got >= MOLT_CAP_PER_CONFIG:
                break
            if ts.max() < a:        # 이 shard가 통째로 윈도우 이전 → 더 과거 shard도 볼 필요 없음
                break
        if not frames:
            print(f"   ! {cfg}: 윈도우({after}~{before})에 해당 행 없음"); continue
        res = pd.concat(frames, ignore_index=True)
        if not full and len(res) > MOLT_CAP_PER_CONFIG:
            res = res.sort_values(col).tail(MOLT_CAP_PER_CONFIG) if col in res.columns else res.head(MOLT_CAP_PER_CONFIG)
        res.to_parquet(out, index=False)
        print(f"   ✓ {len(res):,} rows")


def _record_revision(sha: str, after: str, before: str, full: bool):
    p = ROOT / "research" / "pinned_versions.yaml"
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat()
    p.write_text(
        "# 자동 기록 — 데이터 재현용 버전 핀\n"
        "pinned_versions:\n"
        f"  moltbook_observatory_archive:\n"
        f"    repo: {MOLTBOOK_REPO}\n"
        f"    revision: {sha}\n"
        f"    window: {'FULL' if full else after + '..' + before}\n"
        f"    recorded_at: {stamp}\n"
        f"  reddit_arctic_shift:\n"
        f"    api: {ARCTIC}\n"
        f"    window: {after}..{before}\n"
        f"    subreddits: [{', '.join(SUBREDDITS)}]\n",
        encoding="utf-8",
    )
    print(f"   revision/window 기록 → {p.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser(description="DH-Project 데이터 다운로더")
    ap.add_argument("--launch", action="store_true", help="출시주 윈도우(2026-01-27~)")
    ap.add_argument("--after", help="윈도우 시작 YYYY-MM-DD")
    ap.add_argument("--before", help="윈도우 끝 YYYY-MM-DD")
    ap.add_argument("--full", action="store_true", help="Moltbook 전체 / Reddit 윈도우 무제한")
    ap.add_argument("--reddit-only", action="store_true")
    ap.add_argument("--moltbook-only", action="store_true")
    args = ap.parse_args()

    if args.launch:
        after, before = LAUNCH_AFTER, LAUNCH_BEFORE
    else:
        after = args.after or WINDOW_AFTER
        before = args.before or WINDOW_BEFORE

    do_reddit = not args.moltbook_only
    do_molt = not args.reddit_only
    print(f"=== DH-Project 다운로드  window={after}~{before}  full={args.full} → {RAW} ===\n")

    if do_molt:
        try:
            download_moltbook(after, before, args.full)
        except ImportError as e:
            print("! datasets/huggingface_hub/pandas 미설치 → pip install -r requirements.txt", e)
    if do_reddit:
        download_reddit(after, before, args.full)

    print("\n완료. 노트북 §1.3/§1.4 에서 data/raw/ 경로로 로드하면 됨.")


if __name__ == "__main__":
    main()
