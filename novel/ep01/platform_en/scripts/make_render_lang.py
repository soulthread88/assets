"""Derive build/render_{en,jp}.py from render_v2.py (KO) with locale labels, fonts and typography."""
import sys, os
L = sys.argv[1]
src = open("build/render_v2.py", encoding="utf-8").read()
if L == "en":
    fonts = ('--ui:"Inter",Arial,sans-serif;--tts:"Inter",Arial,sans-serif;--serif:"Source Serif 4",Georgia,serif;--disp:"Playfair Display",Georgia,serif}')
    link = "https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Playfair+Display:wght@700;800;900&display=swap"
    typo = """
.caption,.novel-text p{text-align:left!important;text-justify:auto!important;letter-spacing:0!important}
.logo .l1,.headline h1{font-family:var(--disp)!important;letter-spacing:0!important}
h1{font-family:var(--disp)}
"""
else:
    fonts = ('--ui:"Noto Sans CJK JP","Noto Sans JP",sans-serif;--tts:"Noto Sans CJK JP","Noto Sans JP",sans-serif;--serif:"Noto Serif CJK JP","Noto Serif JP",serif;--disp:"Shippori Mincho","Noto Serif CJK JP",serif}')
    link = "https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@600;700;800&display=swap"
    typo = """
.caption,.novel-text p{line-break:strict!important;overflow-wrap:anywhere!important}
.logo .l1,.headline h1{font-family:var(--disp)!important;letter-spacing:.02em}
h1{font-family:var(--disp);word-break:normal!important;line-break:strict}
"""
R = [
 ("import content_v2 as K", f"import content_{L} as K"),
 ('AUD = f"{ROOT}/audio2"; OUT = f"{ROOT}/out2"; TMP = f"{ROOT}/tmp2"', f'AUD = f"{{ROOT}}/audio_{L}"; OUT = f"{{ROOT}}/out_{L}"; TMP = f"{{ROOT}}/tmp_{L}"'),
 ('--ui:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--tts:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--serif:"Noto Serif KR","Noto Serif CJK KR",serif}', fonts),
 ("@font-face{font-family:'NSK';src:local('Noto Sans CJK KR');}", ""),
 ('<div class="brand-left">전쟁소설</div>', '<div class="brand-left">{E(K.UI["brand_left"])}</div>'),
 ('<span class="l1">장대한 분노</span><span class="l2">호르무즈의 밤</span>', '<span class="l1">{E(K.UI["l1"])}</span><span class="l2">{E(K.UI["l2"])}</span>'),
 ('<span class="tag">소설 속보</span>', '<span class="tag">{E(K.UI["breaking"])}</span>'),
 ('<h1>제 {K.EP_NO}화 - {E(K.SUBTITLE)}</h1>', '<h1>{E(K.UI["headline"])}</h1>'),
 ('<span class="meta-tag">FICTION · 실전 상황</span>', '<span class="meta-tag">{E(K.UI["sit"])}</span>'),
 ('<span class="title">주요사건 타임라인</span>', '<span class="title">{E(K.UI["ticker"])}</span>'),
 ("<span>장대한 분노 · 호르무즈의 밤</span><span>소설</span>", "<span>{E(K.UI['cover_top'])}</span><span>{E(K.UI['cover_kind'])}</span>"),
 ('name = f"epic_fury_ep01_{plat}_ko"', f'name = f"epic_fury_ep01_{{plat}}_{L}"'),
 ("<meta charset='utf-8'><style>", f"<meta charset='utf-8'><link rel='stylesheet' href='{link}'><style>"),
 ("await pg.set_content(j[\"html\"]); await pg.wait_for_timeout(200)",
  "await pg.set_content(j[\"html\"], wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)"),
]
for a, b in R:
    n = src.count(a)
    if n == 0: sys.exit("missing: " + a)
    src = src.replace(a, b)
# locale typography appended to every CSS block
src = src.replace('WIDE_CSS = FONTS + """', 'WIDE_CSS = FONTS + TYPO + """').replace('BAND_CSS = FONTS + """', 'BAND_CSS = FONTS + TYPO + """')
src = src.replace('    return FONTS + f"""\n.cv{{', '    return FONTS + TYPO + f"""\n.cv{{')
src = src.replace("# ---------------- template v2 (desktop)", f"TYPO = '''{typo}'''\n# ---------------- template v2 (desktop)", 1)
# typography rules must win: move TYPO after the block by appending at end of each block instead
src = src.replace('WIDE_CSS = FONTS + TYPO + """', 'WIDE_CSS = FONTS + """').replace('BAND_CSS = FONTS + TYPO + """', 'BAND_CSS = FONTS + """')
src = src.replace("def cover_css(wide):", "WIDE_CSS += TYPO; BAND_CSS += TYPO\ndef cover_css(wide):", 1)
src = src.replace('    return FONTS + TYPO + f"""\n.cv{{', '    return FONTS + f"""\n.cv{{')
src = src.replace('.bar{{margin-top:', '.bar{{margin-top:', 1)
src = src.replace('def header(n, slim):', 'def _cv_typo(s): return s + TYPO\n_cc = cover_css\ncover_css = lambda wide: _cv_typo(_cc(wide))\ndef header(n, slim):', 1)
open(f"build/render_{L}.py", "w", encoding="utf-8").write(src)
import re
left = [m for m in re.findall(r"[가-힣][^\n]{0,20}", src)]
print(L, "hangul left:", left[:10])
