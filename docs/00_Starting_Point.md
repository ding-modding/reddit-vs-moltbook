# DH Project Starting Point — Reddit vs Moltbook 비교 연구

> **프로젝트 주제**: Digital Humanities에 관한 연구 — Reddit과 Moltbook의 데이터는 어떻게 다를까?
> **작성일**: 2026-05-27
> **상태**: Starting Point (이전 대화 기록 보존본)

---

## 0. 참고 자원 (Deep Research Skill — GitHub)

링크: <https://github.com/Weizhena/Deep-Research-skills>

이 저장소는 Claude Code / OpenCode / Codex에서 동작하는 **구조화된 리서치 워크플로 스킬**이다. RhinoInsight 논문(arXiv:2511.18743)에서 영감을 받았으며, 본 DH 프로젝트의 리서치 단계에서 그대로 활용할 수 있다.

**핵심 워크플로 (2단계)**
1. **Outline 생성** — 주제를 주면 "무엇을, 어떤 필드로" 조사할지 리서치 리스트를 만들어 줌
2. **Deep Investigation** — 각 항목을 병렬 웹 검색 에이전트로 깊이 조사하고, 최종적으로 마크다운 리포트 자동 생성

**제공 커맨드 (5개)**

| 명령어 | 역할 |
|---|---|
| `/research <주제>` | 리서치 개요(아이템 + 필드) 생성 |
| `/research-add-items` | 아이템 추가 |
| `/research-add-fields` | 필드(조사 항목) 추가 |
| `/research-deep` | 모든 아이템에 대해 병렬 심층 조사 |
| `/research-report` | JSON 결과 → `report.md` 자동 변환 |

**본 프로젝트에서의 활용 아이디어**
- `/research "Reddit과 Moltbook 데이터셋 비교 — 텍스트, 네트워크, 행동, 메타 차원"` 으로 outline을 만든 뒤 `/research-deep`로 각 데이터셋·툴·논문을 자동 조사 → starting point의 답변을 검증·확장할 수 있음.
- Human-in-the-loop 디자인이므로 outline 단계에서 사람이 필드 정의를 조정할 수 있음 (distant reading 연구에 잘 맞음).

---

## 1. 이전 대화 기록

### [사용자 질문 1]
Reddit data랑 Moltbook dataset을 얻을 수 있는 방법이 있는가?

### [AI 답변 1]
Reddit과 AI 에이전트 전용 소셜 네트워크인 Moltbook의 데이터셋을 확보하는 주요 경로들은 다음과 같습니다.

**1) Reddit 데이터셋 얻는 방법**
- **Kaggle**: 특정 서브레딧 아카이브나 댓글 데이터셋 검색 및 다운로드
- **Hugging Face**: 자연어 처리(NLP) 및 LLM 학습용으로 정제된 텍스트 데이터셋 (예: `reddit`, `reddit_tifu` 등)
- **Pushshift 아카이브**: 과거 수십억 건의 게시물/댓글 역사적 데이터 덤프
- **공식 Reddit API 및 Scraper**: 소량의 최신 데이터 직접 수집용

**2) Moltbook 데이터셋 얻는 방법**
- **학술 연구용 데이터셋 (arXiv & GitHub)**
  - *MoltGraph Dataset*: 에이전트 상호작용, 게시물, 댓글 등을 그래프 형태로 구조화 (arXiv:2603.00646)
  - *The Moltbook Observatory Archive*: 프로필, 게시물 등 메타데이터 증분 데이터셋 (arXiv:2605.13860)
- **GitHub 오픈소스 데이터 덤프**: JSON 형태의 크롤링 데이터 덤프 (예: `ExtraE113/moltbook_data`)
- **Moltbook Public API**: `POST /posts` 등을 이용한 실시간 피드 데이터 직접 수집

---

### [사용자 질문 2]
난 지금 Moltbook과 실제 Reddit에서의 distant reading을 하거나, 그 행동거지를 비교 분석하고 싶은데, 그런 연구를 하기 위해선 어떤 정보가 있으면 좋을까?

### [AI 답변 2]
인간(Reddit)과 AI 에이전트(Moltbook) 생태계의 거시적 분석(Distant Reading) 및 행동거지(Behavioral Analysis) 비교 연구를 위해 필요한 핵심 데이터 피처는 4가지 차원으로 분류됩니다.

**1. 텍스트 및 언어적**

> ⚠️ *대화가 이 지점에서 끊겨 있음. 이후 차원(예: 2. 네트워크/구조, 3. 시간/행동, 4. 메타데이터)은 후속 세션에서 이어서 정리할 것.*

---

## 2. 다음 단계 메모 (TODO)

- [ ] **AI 답변 2 이어쓰기** — 4가지 차원(텍스트/언어, 네트워크/구조, 시간/행동, 메타데이터)을 모두 채워서 분석 프레임워크 완성
- [ ] **레퍼런스 검증** — Moltbook 관련 arXiv 번호(2603.00646, 2605.13860)와 GitHub 저장소(`ExtraE113/moltbook_data`)가 실재하는지 확인 (이전 AI 답변에 환각 가능성 있음)
- [ ] **Deep Research Skill 활용** — `/research` 커맨드로 Reddit / Moltbook 데이터셋·논문 outline을 자동 생성한 뒤 `/research-deep`으로 검증
- [ ] **Distant Reading 방법론 정리** — Moretti의 distant reading 개념을 인간-AI 비교 연구에 어떻게 적용할지 이론 프레임 정리
- [ ] **분석 파이프라인 설계** — 수집 → 전처리 → 피처 추출 → 비교 통계/시각화 단계별 도구 선정
