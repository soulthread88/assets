"""Write render/render_v3_{ko,en,jp}.py from build/render_v2.py (the EP01-final renderer).
v3 = same frames as EP01 final, but every label comes from the content file's UI dict and the
content module / audio / output folders come from environment variables, so any episode can be rendered:
  EF_CONTENT=content_ep02_ko EF_AUDIO=/path/audio_ko EF_OUT=/path/out EF_TMP=/path/tmp python3 render_v3_ko.py shorts reels ..."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src0 = open(os.path.join(HERE, "src", "render_v2_ep01_final.py"), encoding="utf-8").read()
CFG = {
 "ko": ('--ui:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--tts:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--serif:"Noto Serif KR","Noto Serif CJK KR",serif;--disp:"Noto Sans KR","Noto Sans CJK KR",sans-serif}',
        "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Noto+Serif+KR:wght@400;500;700&display=swap", ""),
 "en": ('--ui:"Inter",Arial,sans-serif;--tts:"Inter",Arial,sans-serif;--serif:"Source Serif 4",Georgia,serif;--disp:"Playfair Display",Georgia,serif}',
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Playfair+Display:wght@700;800;900&display=swap",
        ".caption,.novel-text p{text-align:left!important;text-justify:auto!important;letter-spacing:0!important}\n.logo .l1,.headline h1{font-family:var(--disp)!important;letter-spacing:0!important}\nh1{font-family:var(--disp)}\n"),
 "jp": ('--ui:"Noto Sans CJK JP","Noto Sans JP",sans-serif;--tts:"Noto Sans CJK JP","Noto Sans JP",sans-serif;--serif:"Noto Serif CJK JP","Noto Serif JP",serif;--disp:"Shippori Mincho","Noto Serif CJK JP",serif}',
        "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800;900&family=Noto+Serif+JP:wght@400;500;700&family=Shippori+Mincho:wght@600;700;800&display=swap",
        ".caption,.novel-text p{line-break:strict!important;overflow-wrap:anywhere!important}\n.logo .l1,.headline h1{font-family:var(--disp)!important;letter-spacing:.02em}\nh1{font-family:var(--disp);word-break:normal!important;line-break:strict}\n"),
}
for L, (fonts, link, typo) in CFG.items():
    src = src0
    R = [
     ('"""EP01 KR platform videos', '"""EPIC FURY platform MP4 renderer v3 (from the EP01-final renderer) —'),
     ("import content_v2 as K", f"import importlib\nK = importlib.import_module(os.environ.get('EF_CONTENT', 'content_epXX_{L}'))\nLANG = '{L}'"),
     ('AUD = f"{ROOT}/audio2"; OUT = f"{ROOT}/out2"; TMP = f"{ROOT}/tmp2"',
      f'AUD = os.environ.get("EF_AUDIO", f"{{ROOT}}/audio_{L}"); OUT = os.environ.get("EF_OUT", f"{{ROOT}}/out_{L}"); TMP = os.environ.get("EF_TMP", f"{{ROOT}}/tmp_{L}")'),
     ('MEDIA = f"{ROOT}/media"', 'MEDIA = os.environ.get("EF_MEDIA", f"{ROOT}/media")'),
     ('ROOT = "/home/claude/work"', 'ROOT = os.environ.get("EF_ROOT", os.getcwd())'),
     ('--ui:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--tts:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--serif:"Noto Serif KR","Noto Serif CJK KR",serif}', fonts),
     ("@font-face{font-family:'NSK';src:local('Noto Sans CJK KR');}", ""),
     ('<div class="brand-left">전쟁소설</div>', '<div class="brand-left">{E(K.UI["brand_left"])}</div>'),
     ('<span class="l1">장대한 분노</span><span class="l2">호르무즈의 밤</span>', '<span class="l1">{E(K.UI["l1"])}</span><span class="l2">{E(K.UI["l2"])}</span>'),
     ('<span class="tag">소설 속보</span>', '<span class="tag">{E(K.UI["breaking"])}</span>'),
     ('<h1>제 {K.EP_NO}화 - {E(K.SUBTITLE)}</h1>', '<h1>{E(K.UI["headline"])}</h1>'),
     ('<span class="meta-tag">FICTION · 실전 상황</span>', '<span class="meta-tag">{E(K.UI["sit"])}</span>'),
     ('<span class="title">주요사건 타임라인</span>', '<span class="title">{E(K.UI["ticker"])}</span>'),
     ("<span>장대한 분노 · 호르무즈의 밤</span><span>소설</span>", "<span>{E(K.UI['cover_top'])}</span><span>{E(K.UI['cover_kind'])}</span>"),
     ('name = f"epic_fury_ep01_{plat}_ko"', f'name = f"epic_fury_ep{{K.EP2}}_{{plat}}_{L}"'),
     ("<meta charset='utf-8'><style>", f"<meta charset='utf-8'><link rel='stylesheet' href='{link}'><style>"),
     ("await pg.set_content(j[\"html\"]); await pg.wait_for_timeout(200)",
      "await pg.set_content(j[\"html\"], wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)"),
    ]
    for a, b in R:
        if a not in src: sys.exit(f"[{L}] missing: {a[:60]}")
        src = src.replace(a, b)
    src = src.replace("# ---------------- template v2 (desktop)", f"TYPO = '''{typo}'''\n# ---------------- template v2 (desktop)", 1)
    src = src.replace("def cover_css(wide):", "WIDE_CSS += TYPO; BAND_CSS += TYPO\ndef cover_css(wide):", 1)
    src = src.replace('def header(n, slim):', 'def _cv_typo(s): return s + TYPO\n_cc = cover_css\ncover_css = lambda wide: _cv_typo(_cc(wide))\ndef header(n, slim):', 1)
    src = src.replace("sys.path.insert(0, os.path.dirname(__file__))",
                      "sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.environ.get('EF_CONTENT_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content')))", 1)
    assert "sys.path.insert(0, os.environ.get('EF_CONTENT_DIR'" in src
    hang = re.findall(r"[가-힣]+", src.split('"""', 2)[2]) if L != "ko" else []
    open(os.path.join(HERE, "render", f"render_v3_{L}.py"), "w", encoding="utf-8").write(src)
    print(L, "ok", "hangul in code:", sorted(set(hang))[:6])
