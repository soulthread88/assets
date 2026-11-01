# -*- coding: utf-8 -*-
"""Build epic_fury_ep01_longform_{en,jp}.html — same 21-page template v2 as the KO page,
localized for U.S. (en) and Japanese (jp) readers. Usage: python3 make_longform_i18n.py en|jp OUT"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(__file__))
import make_longform_html as B
E = B.E
LANG = sys.argv[1]; OUT = sys.argv[2]
K = importlib.import_module("content_" + LANG)
U = K.UI
B.K = K
B.AUD = f"{B.RAW}/audio/main/novel/ep01/{LANG}_v2"

# fonts / typography per locale
if LANG == "en":
    FONTS = "family=Inter:wght@400;500;600;700;800&amp;family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&amp;family=Playfair+Display:wght@700;800"
    TYPO = """
:root{--ui:"Inter","Helvetica Neue",Arial,sans-serif;--tts:"Inter","Helvetica Neue",Arial,sans-serif;--serif:"Source Serif 4",Georgia,"Times New Roman",serif}
.logo .l1,.headline h1,.novel-heading h2{font-family:"Playfair Display",Georgia,serif;letter-spacing:0}
.caption{font-size:clamp(17px,1.72vw,28px);line-height:1.34;letter-spacing:0;text-align:left;hyphens:manual}
.novel-text p{font-size:clamp(17px,1.78vw,29px);line-height:1.5;letter-spacing:0;text-align:left;hyphens:manual}
.breaking .items,.ticker .items{letter-spacing:0}
@media(max-width:768px){.caption,.novel-text p{font-size:16px}}
"""
    NAV_CUR = "en"
    DESC = ("A war novel inspired by the U.S.–Israeli strikes on Iran on Feb. 28, 2026. An old professor in Tehran, the Pentagon, "
            "the captain of the USS Gerald R. Ford, a CIA analyst and a 7-year-old girl under the rubble — the first morning of the war "
            "through five sets of eyes. Characters and dialogue are fictional.")
    KEYS = ("Epic Fury, Night Over Hormuz, war novel, Iran war fiction, 2026 Iran war, Strait of Hormuz, USS Gerald R. Ford, Tehran, "
            "military thriller, geopolitical thriller, serial fiction, free web novel")
else:
    FONTS = "family=Noto+Sans+JP:wght@400;500;700;800&amp;family=Noto+Serif+JP:wght@400;500;600;700&amp;family=Shippori+Mincho:wght@600;700;800"
    TYPO = """
:root{--ui:"Noto Sans JP","Hiragino Sans","Yu Gothic",Meiryo,sans-serif;--tts:"Noto Sans JP","Hiragino Sans","Yu Gothic",Meiryo,sans-serif;--serif:"Noto Serif JP","Hiragino Mincho ProN","Yu Mincho",serif}
.logo .l1,.headline h1,.novel-heading h2{font-family:"Shippori Mincho","Noto Serif JP",serif;letter-spacing:.02em}
.caption,.novel-text p{line-break:strict;word-break:normal;overflow-wrap:anywhere;font-feature-settings:"palt" 0;letter-spacing:.01em}
.caption{font-size:clamp(17px,1.95vw,31px);line-height:1.42}
.novel-text p{font-size:clamp(17px,1.95vw,31px);line-height:1.62}
@media(max-width:768px){.caption,.novel-text p{font-size:16px}}
"""
    NAV_CUR = "jp"
    DESC = ("2026年2月28日、米・イスラエルによる対イラン作戦に着想を得た戦争小説。テヘランの老教授、国防総省、空母フォードの艦長、"
            "CIAの分析官、がれきの下の七歳の少女――開戦初日の朝を五つのまなざしで追う。登場人物と会話は創作です。")
    KEYS = ("エピック・フューリー, ホルムズの夜, 戦争小説, イラン戦争 小説, 2026年 イラン戦争, ホルムズ海峡, 空母フォード, テヘラン, "
            "ミリタリー・スリラー, 地政学スリラー, 連載小説, 無料 Web小説")

def header(n, slim):
    return (f'<header class="header{" header--slim" if slim else ""}">\n  <div class="brand-left">{E(U["brand_left"])}</div>\n'
            f'  <div class="logo"><span class="l1">{E(U["l1"])}</span><span class="l2">{E(U["l2"])}</span></div>\n'
            f'  <div class="datetime"><span class="date">{E(K.DATE)}</span><span class="part">{n}/21</span></div>\n</header>\n')
B.header = header

def media_el(k, alt=False):
    m = B.MAN[k]; u = B.media_url(k)
    if m["type"] == "video":
        return f'<video autoplay muted loop playsinline preload="metadata"><source src="{u}{"#t=3" if alt else ""}" type="video/mp4">{E(U["novideo"])}</video>'
    return f'<img src="{u}" alt="">'
B.media_el = media_el
B.tools = lambda: (f'<div class="imgtools" hidden><button type="button" class="btn-rep">{E(U["rep"])}</button>'
                   f'<button type="button" class="btn-del">{E(U["dele"])}</button><input type="file" accept="image/*,video/*" hidden></div>')

def stage(pg):
    s = B.stage(pg)
    rep = [(f'ep01_ko_p', f'ep01_{LANG}_p'), ('aria-label="내레이션 재생"', f'aria-label="{E(U["aria"])}"'),
           ('FICTION · 실전 상황', E(U["sit"])), ('<span class="tag">소설 속보</span>', f'<span class="tag">{E(U["breaking"])}</span>'),
           ('<span class="title">주요사건 타임라인</span>', f'<span class="title">{E(U["ticker"])}</span>'),
           ('소설 속 전쟁 상황 속보', 'news bulletin'), ('소설 본문', 'novel text'),
           (f'<h1>제 {K.EP_NO}화 - {E(K.SUBTITLE)}</h1>', f'<h1>{E(U["headline"])}</h1>')]
    for a, b in rep: s = s.replace(a, b)
    return s

xcss = B.EXTRA_CSS.replace("/* ---- 사이트 메뉴(영상 화면 밖): Kor | Eng · Dark/Light ---- */", "/* site menu (outside the video frame) */") \
    .replace("/* 화면별 미디어 출처: 본문보다 5px 이상 작은 이탤릭, 원출처 링크 */", "/* media credit: italic, >=5px smaller than body, linked to source */") \
    .replace("/* 미디어 박스 교체·삭제(클릭할 때만 표시) */", "/* media box replace/delete (shown on click only) */") \
    .replace("/* 라이트 모드: 화면(영상) 밖의 페이지 바탕과 메뉴만 밝게 — 영상 화면 안의 글자는 어두운 영상 위에 그대로 둔다 */", "/* light mode: page chrome only */") \
    .replace("/* 영상 녹화용: ?record 로 열면 메뉴·버튼을 숨긴다 */", "/* ?record hides menu and buttons for screen recording */")
xjs = B.EXTRA_JS.replace("HormuzMedia2026__ep01_longform_ko__", f"HormuzMedia2026__ep01_longform_{LANG}__") \
    .replace("'🌙 Dark' : '☀ Light'", f"'{U['dark']}' : '{U['light']}'") \
    .replace("// 메뉴(언어·테마) + 미디어 박스 교체/삭제(HormuzDB: IndexedDB → localStorage → 메모리)", "// menu (language/theme) + media replace/delete (HormuzDB: IndexedDB → localStorage → memory)")
script = B.SCRIPT.replace("// 자막(캡션)이 먼저 보이고, 내레이션은 0.5초 뒤에 시작한다.", "// caption first; narration starts 0.5 s later.")

def nav():
    items = [("ko", "Kor", "epic_fury_ep01_longform_ko.html"), ("en", "Eng", "epic_fury_ep01_longform_en.html"), ("jp", "Jpn", "epic_fury_ep01_longform_jp.html")]
    out = []
    for code, lab, href in items:
        hl = {"ko": "ko", "en": "en", "jp": "ja"}[code]
        cur = ' aria-current="page"' if code == NAV_CUR else ""
        out.append(f'<a href="{href}"{cur} lang="{hl}">{lab}</a>')
    return '<span class="lang">' + ' <span>|</span> '.join(out) + '</span>'

stages = "".join(stage(p) for p in K.PAGES)
T = U["title"]
doc = f"""<!DOCTYPE html>
<html lang="{U['html_lang']}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(T)}</title>
<meta name="description" content="{E(DESC)}">
<meta name="keywords" content="{E(KEYS)}">
<meta property="og:type" content="article">
<meta property="og:locale" content="{'en_US' if LANG=='en' else 'ja_JP'}">
<meta property="og:title" content="{E(T)}">
<meta property="og:description" content="{E(DESC)}">
<meta property="og:image" content="{B.RAW}/imgs/main/novel/ep01/ep01_og_{LANG}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(T)}">
<meta name="twitter:description" content="{E(DESC)}">
<link rel="alternate" hreflang="ko" href="https://github.com/soulthread88/htmls/blob/main/novel/epic_fury_ep01_longform_ko.html">
<link rel="alternate" hreflang="en" href="https://github.com/soulthread88/htmls/blob/main/novel/epic_fury_ep01_longform_en.html">
<link rel="alternate" hreflang="ja" href="https://github.com/soulthread88/htmls/blob/main/novel/epic_fury_ep01_longform_jp.html">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS}&amp;display=swap">
<style>
{B.CSS}
{xcss}
{TYPO}
</style>
</head>
<body>
<header class="site-bar"><span class="ttl">{E(T)}</span>
<nav>{nav()}
<button type="button" id="theme-btn">{E(U['light'])}</button></nav></header>
{stages}
{script}
{xjs}
</body>
</html>
"""
import re as _re
doc = _re.sub(r"/\*[^*]*?[가-힣][^*]*?\*/", "", doc)
doc = _re.sub(r"(?m)^([ \t]*)//[^\n]*[가-힣][^\n]*$", "", doc)
doc = _re.sub(r"[ \t]+//[^\n'\"]*[가-힣][^\n'\"]*$", "", doc, flags=_re.M)
open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", OUT, len(doc))
