# EPIC FURY 플랫폼 MP4 템플릿 v3 (EP01 최종본 기준)

EP01 최종 영상 24개(+ 세로 롱폼 3개)를 만든 화면 구성, 렌더러, 내레이션 절차를 그대로 묶은 템플릿이다.
새 화는 **내용 파일 하나만 채우면** 9개 플랫폼 × 한·영·일 MP4가 EP01과 같은 모양으로 나온다.

## 플랫폼 규격 (EP01 최종본과 동일)

| 플랫폼 | 해상도 | 배치 | 기본 쪽 (21쪽 중) | 비고 |
|---|---|---|---|---|
| longform | 3840×2160 | wide (16:9 원본 화면) | 1–21 | 8분 이상이어야 함 |
| longform_mobile | 2160×3840 | band (세로 띠) | 1–21 | 휴대폰 세로용 롱폼 |
| x | 3840×2160 | wide | 1, 2, 3 | |
| facebook | 3840×2160 | wide | 1, 6, 7 | |
| shorts | 2160×3840 | band | 1–5 | 3분 이내 |
| reels | 2160×3840 | band | 8, 9, 18, 19 | |
| tiktok | 2160×3840 | band | 3, 16, 17, 20, 21 | |
| threads | 2160×2700 | band | 1, 12–15 | |
| feeds | 2160×2700 | band | 10, 11 | |

- 21쪽 = 속보 5쪽(1–5) + 장면 8개 × 2화면(6–21). 화면 문장이 곧 내레이션.
- 영상 한 편 = 표지(플랫폼별 제목) → 고른 쪽들 → 끝 카드. 각 쪽 = 0.5초 앞여백 + 내레이션 + 꼬리(롱폼 1.2초, 나머지 0.6초).
- wide: 템플릿 v2 데스크톱 화면(1600×900 CSS)을 그대로 4K로. 헤더 · 에피소드 제목 · 영상 위 캡션 · 소설 속보 · 주요사건 타임라인(흐름).
- band: 1080 CSS 폭 띠(헤더 · 제목 · 영상+글 · 속보)를 화면 0.41(9:16) / 0.45(4:5) 높이에 놓고, 위아래는 같은 영상을 흐리게 깐다. 글이 길면 30px까지 자동으로 줄인다.
- 상황 태그에는 FICTION을 넣지 않는다: 실전 상황 / SITUATION REPORT / 戦況 (2026-11-02 원칙).
- 오디오: 내레이션 −16 LUFS로 정규화, 30fps, H.264 high, 95 MB 넘는 파일은 GitHub Git LFS.

## 들어 있는 것

| 폴더 | 내용 |
|---|---|
| `content/content_epXX_{ko,en,jp}.py` | 채울 내용 파일. `[[...]]` 자리 + 미디어 키 + 플랫폼별 쪽·표지 |
| `render/render_v3_{ko,en,jp}.py` | MP4 렌더러 (EP01 렌더러와 같은 프레임. 시험 결과 EP01 영상과 평균 픽셀 차 0.4/255) |
| `tts/tts_typecast_ko.py` | 한국어 내레이션 — Typecast 인화 |
| `tts/tts_edge.py`, `tts/make_durations.py` | 영어·일본어 내레이션 — 무료 Edge 음성(Brian / Keita). WebSocket이 필요해 PC에서 실행 |
| `html/novel_{kr,en,jp}_{플랫폼}_epXX_template_v3.html` | 27개 미리보기 템플릿: MP4와 같은 화면을 브라우저에서 넘겨 보며 글 길이·사진을 확인 |
| `preview/` | 플랫폼별 화면 견본(표지 · 속보 · 장면 · 끝 카드) |
| `make_*.py` | 위 파일들을 EP01 최종 빌드에서 다시 만드는 생성기 |

## 새 화 만드는 순서

1. `content/content_epXX_ko.py`를 `content_ep02_ko.py`로 복사해 `[[...]]`를 채운다. 영어·일본어도 같은 방식(정본 번역본 문장 사용).
   - 미디어 키는 `media/manifest.json`에 등록한 이번 화 사진·영상 키로 바꾼다(작가·라이선스·원본 링크 포함).
   - 플랫폼별 쪽 번호와 표지 제목은 이번 화의 고리가 되는 장면으로 고른다.
2. 맞춤법 검사: 한국어 korean-grammar-checker, 영어 human-touch, 일본어 stop-ai-slop-jp.
3. 내레이션
   - KO: `TYPECAST_API_KEY=… EF_CONTENT=content_ep02_ko EF_AUDIO=./audio_ko python3 tts/tts_typecast_ko.py`
   - EN/JP(PC): `EF_CONTENT=content_ep02_en EF_AUDIO=./audio_en python tts/tts_edge.py en` → mp3를 렌더 컴퓨터로 옮긴 뒤 `python3 tts/make_durations.py en`
   - 롱폼 예상 길이가 480초(8분) 이상인지 확인.
4. 미리보기: `python3 make_html_templates.py ko shorts ./html` (내용 파일을 바꿨다면 `EF_CONTENT=content_ep02_ko`). 글이 넘치지 않는지 본다.
5. 렌더:
   ```
   EF_ROOT=. EF_MEDIA=./media EF_CONTENT=content_ep02_ko EF_AUDIO=./audio_ko EF_OUT=./out_ko EF_TMP=./tmp_ko \
     python3 render/render_v3_ko.py longform longform_mobile x facebook shorts reels tiktok threads feeds
   ```
   - 4K라 2코어 기준 영상 100초당 약 13분. 한 번에 2시간을 넘기지 않게 플랫폼 몇 개씩 나눠 돌린다(중간 산출물이 남아 이어서 렌더된다).
   - 디스크가 차면 끝난 플랫폼의 `tmp_*` 폴더를 지운다.
6. 검사: 길이(ffprobe), 프레임 몇 장 눈으로 확인, 자막 `.srt` 함께 생성됨.
7. 올리기: `videos/novel/epNN/platform_{ko,en,jp}/`(95 MB 초과는 LFS), `audio/novel/epNN/{ko,en,jp}_v2/`, 로컬 `G:\내 드라이브\ai\github\novels\<화>\platforms\`.

## 고정 값 (바꾸지 않는 것)
- 색: 남색 #06152d, 금색 #f4bd3f, 빨강 #d92d3a / 글꼴: KO Noto Sans·Serif KR, EN Inter·Source Serif 4·Playfair Display, JP Noto Sans·Serif JP·Shippori Mincho
- 표지: 상단 시리즈명·종류, FICTION·EP 배지, 큰 제목, 금색 부제, 금색 막대
- 끝 카드: 다음 화 안내 + "픽션 · AI 내레이션"
- 미디어: 4K 이상 무료 출처(Wikimedia Commons, Pexels, Pixabay, Unsplash), 출처 표기 필수
