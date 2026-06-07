# reddit-vs-moltbook — Reddit vs Moltbook 비교 연구

> Digital Humanities 연구: **인간(Reddit) vs AI 에이전트(Moltbook)** 데이터는 어떻게 다른가?
> Distant reading + 행동 비교 분석 파이프라인.

## 폴더 구조

```
reddit-vs-moltbook/
├── README.md                  ← 이 파일 (실행 안내)
├── requirements.txt           ← 로컬 실행용 의존성
├── .gitignore
│
├── notebooks/
│   └── colab_analysis.ipynb   ← 메인 분석 노트북 (Colab/로컬 겸용)
│
├── docs/
│   ├── 00_Starting_Point.md   ← 프로젝트 출발점 / 이전 대화 보존본
│   └── research_report.md     ← Deep Research 검증 리포트 (§6 패치 근거)
│
├── research/
│   ├── outline.yaml           ← 리서치 개요 (16 items)
│   ├── fields.yaml            ← 조사 필드 정의
│   └── results/               ← 항목별 deep-research JSON (17개)
│
├── data/
│   ├── raw/                   ← (gitignore) 다운로드한 원본 덤프 보관
│   └── processed/             ← (gitignore) 전처리 산출물
│
└── dh_reddit_moltbook/        ← 노트북 런타임 폴더 (자동 생성/사용)
    ├── data/  cache/  outputs/
```

## 실행 방법

### A. 로컬 (Jupyter)

```bash
cd reddit-vs-moltbook                                # 저장소 루트로 이동
python -m venv .venv && .venv\Scripts\activate      # (선택) 가상환경
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python scripts/smoke_test.py                         # 환경 점검 (10초)
jupyter lab notebooks/colab_analysis.ipynb
```

노트북은 실행 위치와 무관하게 런타임 산출물을 repo 루트의 `dh_reddit_moltbook/`에 저장한다 (셀 4에서 자동 처리).

### B. Google Colab

`notebooks/colab_analysis.ipynb`를 Colab에 업로드 → 셀 3이 의존성을 설치 (~3분) → 위에서부터 순서대로 실행. Colab에서는 런타임 폴더가 `/content/dh_reddit_moltbook/`에 생성된다.

## 어떤 데이터를 불러올까 (§1)

6개 로더는 **플랫폼당 하나씩만** 고르면 비교가 성립한다 (같은 플랫폼 내에서는 서로 대안).

| 셀 | 플랫폼 | 역할 | 실행 |
|---|---|---|---|
| §1.1 PRAW API | Reddit | 실시간·소량, 인증 필요 | 선택 |
| §1.2 HF webis-tldr-17 | Reddit | 정제 코퍼스. parent_id·timestamp 없음 → 네트워크/시간 분석 불가 | 대안 |
| **§1.3 Academic Torrents 덤프** | Reddit | created_utc·parent_id 완비, 2026-Q1 매칭 슬라이스 | **✅ 권장** |
| **§1.4 HF Observatory Archive** | Moltbook | 게시물+메타데이터 메인 소스 | **✅ 권장** |
| §1.5 Public API | Moltbook | 실시간 피드 보충용 | 선택 |
| §1.6 MoltGraph (.graphml) | Moltbook | 기성 에이전트 그래프 (§4 대체용) | 선택 |

**최소 조합: §1.3 + §1.4** → 텍스트·네트워크·시간·커뮤니티 4개 차원 비교가 모두 동작.

## 데이터 받기 (scripts/download_data.py)

이 환경(Claude)에서는 네트워크 제약으로 데이터를 직접 못 받아서, **네 PC에서 실행하는 다운로더**를 넣어뒀다. 받은 파일은 `data/raw/`에 저장된다.

```bash
python scripts/download_data.py              # 빠른 샘플 (서브레딧당 ~5천, Moltbook config당 ~5만)
python scripts/download_data.py --full       # 전체 윈도우 (수 GB, 오래 걸림)
python scripts/download_data.py --moltbook-only   # / --reddit-only
```

- **§1.4 Moltbook**: HF `SimulaMet/moltbook-observatory-archive`에서 parquet(`posts/comments/agents`)을 받고, revision SHA를 `research/pinned_versions.yaml`에 자동 기록.
- **§1.3 Reddit**: 3.4TB 토렌트 대신 Arctic Shift API로 2026-01-27~04-14 매칭 슬라이스만 ndjson으로. 비교군 서브레딧은 스크립트 상단 `SUBREDDITS` 리스트에서 수정.

노트북에서 받은 로컬 파일 로드:

```python
df_reddit   = load_local_reddit("posts")      # §1.3 셀
df_moltbook = load_local_moltbook("posts")    # §1.4 셀
```

## 분석 차원

- **§2 공통 스키마 + MBC-20 필터** — 두 플랫폼 필드 통일 후, Moltbook의 거래성 페이로드(~63%)를 분리하고 discursive 서브셋(~37%)을 분석.
- **§3 텍스트/언어** — 길이, TTR, 1인칭 비율, 가독성, 감정, BERTopic 토픽 분포(스레드/작성자 풀링).
- **§4 네트워크** — reply tree 깊이/폭/분기.
- **§5 시간/행동** — 시간대·요일 리듬(circadian), 버스트 감지.
- **§6 커뮤니티/작성자** — 커뮤니티 프로필, 작성자 활동 분포.
- **§7 Moltbook 특화** — 모델 provenance(claude/gpt/…), 사람 contamination 휴리스틱.
- **§8 종합** — 요약 테이블, KS·Mann-Whitney 검정, radar chart.

## 다음 단계 (TODO)

1. Observatory Archive 다운로드 → HF revision SHA를 `research/outline.yaml`의 `pinned_versions`에 기록.
2. Reddit 2026-01-27~04-14 매칭 슬라이스 추출 (RS_/RC_ 2026-Q1).
3. §1.3 + §1.4 실행 → §2 MBC-20 필터 sanity check (discursive ~37% 확인).
4. §3 토픽모델링 + §8 요약 실행.

## 라이선스

이 저장소는 **듀얼 라이선스**다.

- **코드** (`notebooks/`, `scripts/`) — [MIT License](LICENSE)
- **데이터·문서·결과물** (`docs/`, `research/`, `presentation/`) — [CC BY 4.0](LICENSE-DATA)

활용·인용 시 출처를 밝혀 주세요. 단, repo에 포함되지 않은 **원본 Reddit/Moltbook 데이터**(`data/`, gitignore 처리됨)는 각 플랫폼의 이용약관을 따릅니다.
