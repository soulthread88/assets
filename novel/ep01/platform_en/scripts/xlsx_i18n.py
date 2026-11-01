# -*- coding: utf-8 -*-
"""Add EN/JP sheets to the EP01 review workbook (3차: 영어·일본어판)."""
import json, os, subprocess, sys, importlib
sys.path.insert(0, os.path.dirname(__file__))
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
SRC = "out2/epic_fury_ep01_ko_video_review.xlsx"; DST = "out6/epic_fury_ep01_video_review_ko_en_jp.xlsx"
os.makedirs("out6", exist_ok=True)
wb = openpyxl.load_workbook(SRC)
for n in ["3차 변경(영어·일본어)", "3차 파일 스펙", "3차 대본 EN", "3차 대본 JP", "3차 맞춤법 검토", "3차 저장 위치"]:
    if n in wb.sheetnames: del wb[n]
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="06152D"); thin = Side(style="thin", color="C9CED6")
def sheet(name, head, rows, widths):
    ws = wb.create_sheet(name); ws.append(head)
    for c in ws[1]: c.font = H; c.fill = HF; c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in rows: ws.append(r)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(vertical="top", wrap_text=True); c.border = Border(bottom=thin)
    for i, w in enumerate(widths): ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"; return ws
RAW = "https://raw.githubusercontent.com/soulthread88"; GH = "https://github.com/soulthread88"
changes = [
 (1, "EN·JP 롱폼 HTML", "한글 롱폼(템플릿 v2, 21쪽)을 기준으로 미국판·일본판 제작", "epic_fury_ep01_longform_en.html / _jp.html (htmls/novel)"),
 (2, "EN 표기", "미국식: Feb. 28, 2026 · 9:45 a.m.(AP), 굽은 따옴표(“ ” ’), 왼쪽 정렬, Inter + Source Serif 4 + Playfair Display", "적용"),
 (3, "JP 표기", "일본식: 2026年2月28日 · 午前9時45分, 「」 『』, line-break:strict, Noto Sans/Serif JP + Shippori Mincho, 소설 본문 한자 숫자", "적용"),
 (4, "EN·JP 문장", "기존 정본 htmls/novel/epic_fury_ep01_en.html·_jp.html 문장을 21쪽 구조에 맞춰 배치", "8장면 16쪽 + 뉴스 5쪽"),
 (5, "언어 메뉴", "모든 페이지 Kor | Eng | Jpn + Dark/Light, 한국어 롱폼에도 Jpn 추가", "적용"),
 (6, "EN·JP 내레이션", "무료 Edge 음성: en-US-BrianNeural, ja-JP-KeitaNeural(속도 -5%). 이 작업 환경은 Edge(WebSocket)에 접속할 수 없어 사용자 PC에서 생성", "각 30개 mp3 → audio/novel/ep01/en_v2, jp_v2"),
 (7, "EN 낭독 보정", "p09 '0115.' → 'One-fifteen.'(TTS가 숫자를 끊어 읽지 않도록)", "적용"),
 (8, "EN·JP 플랫폼 영상", "한글 v2와 같은 구조·프레임(표지 → 쪽 → 끝 카드)으로 8개 플랫폼 × 2개 언어 렌더", "3840×2160 / 2160×3840 / 2160×2700"),
 (9, "플랫폼 동적 HTML", "플랫폼 × ko·en·jp 21개: 영상과 같은 화면(렌더 레이어 그대로) + 실시간 미디어·내레이션·자동 넘김", "htmls/novel/epic_fury_ep01_<플랫폼>_<언어>.html"),
 (10, "블로그", "Tistory·Naver·WordPress·Substack × ko·en·jp 12개: 미리보기 + 플랫폼용 본문 복사(WordPress는 블록 주석, Naver·Substack은 영상 대신 링크 이미지)", "htmls/novel/epic_fury_ep01_blog_<플랫폼>_<언어>.html"),
 (11, "히어로·OG", "언어별 30:9 히어로(3840×1152)와 1200×630 OG 카드", "imgs/novel/ep01/ep01_hero_*.jpg, ep01_og_*.jpg"),
 (12, "KO 맞춤법", "포토맥강·알보르즈산맥·무산담반도·호르무즈해협(외래어 지명 + 강·산맥·반도·해협 붙여 씀), '해 주소서'(보조용언 띄어 씀)", "롱폼 HTML + Feeds·Reels·TikTok·Longform 영상 다시 렌더"),
 (13, "로컬 저장", "G:\\내 드라이브\\ai\\github\\novels\\platforms\\100126\\{imgs,videos,htmls,audio} (기존 폴더명이 novels)", "GitHub에서 내려받아 저장"),
]
sheet("3차 변경(영어·일본어)", ["No", "대상", "변경 내용", "결과"], changes, [5, 20, 80, 50])
spec = []
for lang, od in (("ko", "out2"), ("en", "out_en"), ("jp", "out_jp")):
    K = importlib.import_module({"ko": "content_v2", "en": "content_en", "jp": "content_jp"}[lang])
    for plat, v in K.PLATFORMS.items():
        f = f"{od}/epic_fury_ep01_{plat}_{lang}.mp4"
        if os.path.exists(f):
            d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
            mb = round(os.path.getsize(f) / 1e6, 1)
        else: d, mb = None, None
        spec.append((lang, plat, os.path.basename(f), f"{v[0]}×{v[1]}", round(d, 1) if d else "렌더 중", mb, v[4], ", ".join(map(str, v[2]))))
sheet("3차 파일 스펙", ["언어", "플랫폼", "파일", "해상도", "길이(초)", "용량(MB)", "표지 제목", "쪽"], spec, [6, 10, 34, 12, 10, 10, 26, 22])
for lang, nm in (("en", "3차 대본 EN"), ("jp", "3차 대본 JP")):
    K = importlib.import_module("content_" + lang); D = json.load(open(f"audio_{lang}/durations.json"))
    rows = [(p["n"], "뉴스" if p["kind"] == "news" else "소설", p.get("loc") or p.get("tag"), p.get("h2") or "", p["text"], D[f"p{p['n']:02d}"]["dur"], p["media"]) for p in K.PAGES]
    sheet(nm, ["쪽", "유형", "위치/장면", "소제목", "화면 문장 = 내레이션", "음성(초)", "미디어"], rows, [5, 7, 30, 24, 90, 9, 16])
review = [
 ("KO", "korean-grammar-checker", "외래어 지명 붙여 쓰기 4곳, 보조용언 1곳 수정. 나머지 확실한 오류 없음", "적용"),
 ("EN", "human-touch + pyspellchecker + codespell", "철자 오류 0(미등록어는 모두 고유명사). AP식 시각·날짜 확인, 굽은 따옴표 적용, 'under way' → 'underway'", "적용"),
 ("JP", "stop-ai-slop-jp(기호·표기 점검)", "반각 문장부호·중복 조사·반각 가나 없음. 소설 본문 숫자 표기 통일: 200メートル → 二百メートル, 20% → 二十パーセント", "적용"),
]
sheet("3차 맞춤법 검토", ["언어", "스킬·도구", "결과", "조치"], review, [6, 34, 80, 10])
loc = [
 ("롱폼 HTML ko·en·jp", f"{GH}/htmls/tree/main/novel", "epic_fury_ep01_longform_{ko,en,jp}.html"),
 ("플랫폼 동적 HTML 21개", f"{GH}/htmls/tree/main/novel", "epic_fury_ep01_<x|facebook|shorts|reels|tiktok|threads|feeds>_<ko|en|jp>.html"),
 ("블로그 HTML 12개", f"{GH}/htmls/tree/main/novel", "epic_fury_ep01_blog_<tistory|naver|wordpress|substack>_<ko|en|jp>.html"),
 ("EN 영상", f"{GH}/videos/tree/main/novel/ep01/platform_en", "8개 MP4 (95 MB 넘는 파일은 Git LFS)"),
 ("JP 영상", f"{GH}/videos/tree/main/novel/ep01/platform_jp", "8개 MP4 (95 MB 넘는 파일은 Git LFS)"),
 ("EN·JP 내레이션", f"{GH}/audio/tree/main/novel/ep01", "en_v2 / jp_v2 (Edge TTS 30개씩)"),
 ("히어로·OG", f"{GH}/imgs/tree/main/novel/ep01", "ep01_hero_{ko,en,jp}.jpg, ep01_og_{ko,en,jp}.jpg"),
 ("자막·스크립트", f"{GH}/assets/tree/main/novel/ep01", "platform_en / platform_jp: srt, 빌드 스크립트"),
 ("로컬", "G:\\내 드라이브\\ai\\github\\novels\\platforms\\100126", "imgs · videos · htmls · audio"),
]
sheet("3차 저장 위치", ["종류", "위치", "내용"], loc, [22, 70, 60])
wb.save(DST); print("saved", DST)
