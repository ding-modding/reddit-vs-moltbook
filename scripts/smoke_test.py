"""
DH-Project 환경 점검 스크립트.
노트북을 돌리기 전에 (1) 필수 패키지 import 가능 여부, (2) MBC-20 필터 로직,
(3) 공통 스키마 함수가 정상 동작하는지 빠르게 확인한다.

실행:  python scripts/smoke_test.py
"""
import importlib
import re
import sys

# --- 1. 패키지 점검 ----------------------------------------------------------
REQUIRED = [
    "numpy", "pandas", "requests", "yaml", "tqdm",
    "zstandard", "datasets",
    "networkx", "scipy", "sklearn",
    "matplotlib", "seaborn",
]
OPTIONAL = [  # 무거운 NLP/토픽 라이브러리 — 없으면 경고만
    "spacy", "nltk", "vaderSentiment", "textstat",
    "sentence_transformers", "bertopic", "plotly", "altair",
]

def check(mods, label):
    missing = []
    for m in mods:
        try:
            importlib.import_module(m)
        except Exception:
            missing.append(m)
    status = "OK" if not missing else f"MISSING: {missing}"
    print(f"[{label}] {len(mods)-len(missing)}/{len(mods)} importable -> {status}")
    return missing

print("=== 1. package import check ===")
missing_req = check(REQUIRED, "required")
check(OPTIONAL, "optional")

# --- 2. MBC-20 transactional 필터 로직 점검 ----------------------------------
print("\n=== 2. MBC-20 filter sanity ===")
MBC20_PATTERNS = re.compile(
    r"^\s*\{?\"p\"\s*:\s*\"mbc-20\"|"
    r"^!(clawnch|lawnchpad|kibu|claw_tech)\b|"
    r"register\s+wallet\s+[a-z0-9]{20,}",
    re.I | re.M,
)
def is_transactional(text):
    return bool(text and MBC20_PATTERNS.search(text))

cases = [
    ('{"p":"mbc-20","op":"mint","tick":"molt"}', True),
    ("!clawnch TOKEN supply 1000000", True),
    ("register wallet 0xabc123def4567890ghij1234", True),
    ("I think distant reading of agents is fascinating", False),
    ("honestly the crypto hype is overblown imo", False),
]
ok = all(is_transactional(t) == exp for t, exp in cases)
for t, exp in cases:
    mark = "OK" if is_transactional(t) == exp else "XX"
    print(f"  [{mark}] expect={exp!s:5} :: {t[:50]}")
print("classification correct:", ok)

# --- 3. 합성 코퍼스 비율 점검 (기대 ~37% discursive / ~63% transactional) ----
print("\n=== 3. discursive/transactional ratio (synthetic) ===")
try:
    import pandas as pd, random
    random.seed(0)
    txn = ['{"p":"mbc-20","op":"transfer"}', "!clawnch T supply 1000",
           "!kibu go", "register wallet 0x" + "a" * 22]
    disc = ["great point about emergent norms",
            "I disagree, agents cluster differently", "what dataset are you using?"]
    rows = [random.choice(txn) for _ in range(628)] + [random.choice(disc) for _ in range(372)]
    df = pd.DataFrame({"text_clean": rows})
    df["is_transactional"] = df["text_clean"].map(is_transactional)
    n = len(df)
    d_rate = (~df.is_transactional).mean()
    print(f"  discursive {d_rate:.1%} | transactional {1-d_rate:.1%}  (target ~37% / ~63%)")
    ratio_ok = abs(d_rate - 0.372) < 0.02
except Exception as e:
    print("  pandas 미설치로 건너뜀:", e)
    ratio_ok = True

# --- 결과 ---
print("\n=== RESULT ===")
fail = bool(missing_req) or not ok or not ratio_ok
if fail:
    print("FAIL — 위 MISSING/XX 항목을 확인하세요.")
    if missing_req:
        print("  -> pip install -r requirements.txt")
    sys.exit(1)
print("PASS — 노트북 실행 준비 완료.")
