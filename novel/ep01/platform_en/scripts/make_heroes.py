"""Language heroes for EP01: 30:9 hero (3840x1152) and 1200x630 OG card, rendered from the media library."""
import asyncio, sys, os, html, importlib, base64
sys.path.insert(0, os.path.dirname(__file__))
E = html.escape
IMG = open("media/" + __import__("json").load(open("media/manifest.json"))["img_ford_deck"]["file"], "rb").read()
B64 = "data:image/jpeg;base64," + base64.b64encode(IMG).decode()
CFG = {
 "ko": ("content_v2", "장대한 분노 · 호르무즈의 밤", "제1화", "'Noto Sans CJK KR',sans-serif", "소설"),
 "en": ("content_en", "Epic Fury: Night Over Hormuz", "Episode 1", "'Playfair Display',Georgia,serif", "NOVEL"),
 "jp": ("content_jp", "エピック・フューリー：ホルムズの夜", "第1話", "'Shippori Mincho','Noto Serif CJK JP',serif", "小説"),
}
LINK = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@800;900&family=Shippori+Mincho:wght@800&family=Inter:wght@700;800&display=swap"
def doc(lang, w, h, big):
    mod, series, ep, ff, kind = CFG[lang]; K = importlib.import_module(mod)
    s = big / 100
    return f"""<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='{LINK}'><style>
body{{margin:0;width:{w}px;height:{h}px;position:relative;overflow:hidden;background:#06152d;font-family:Inter,'Noto Sans CJK KR','Noto Sans CJK JP',sans-serif}}
.bg{{position:absolute;inset:0;background:url({B64}) center 40%/cover;filter:brightness(.82) saturate(.9)}}
.g{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(2,9,20,.9) 0%,rgba(2,9,20,.7) 42%,rgba(2,9,20,.15) 80%)}}
.t{{position:absolute;left:{int(60*s)}px;top:50%;transform:translateY(-50%);max-width:66%}}
.p span{{display:inline-block;font-weight:800;font-size:{int(26*s)}px;padding:.15em .55em;margin-right:.5em;letter-spacing:.05em}}
.a{{background:#e0383e;color:#fff}}.b{{border:2px solid #f4bd3f;color:#f4bd3f}}
h1{{margin:.35em 0 .2em;font-family:{ff};font-weight:900;font-size:{int(84*s)}px;line-height:1.1;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.6)}}
.s{{color:#f4bd3f;font-weight:700;font-size:{int(30*s)}px}}
.k{{position:absolute;right:{int(60*s)}px;top:{int(40*s)}px;color:#f4bd3f;font-weight:800;font-size:{int(22*s)}px}}
</style></head><body><div class=bg></div><div class=g></div><div class=k>{E(kind)}</div>
<div class=t><div class=p><span class=a>FICTION</span><span class=b>EP 01</span></div><h1>{E(K.SUBTITLE)}</h1><div class=s>{E(series)} · {E(ep)}</div></div></body></html>"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for lang in CFG:
            for name, w, h, big, dpr in (("hero", 1920, 576, 140, 2), ("og", 1200, 630, 100, 1)):
                ctx = await br.new_context(viewport=dict(width=w, height=h), device_scale_factor=dpr); pg = await ctx.new_page()
                await pg.set_content(doc(lang, w, h, big), wait_until="networkidle"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
                out = f"out5/ep01_{name}_{lang}.jpg"; await pg.screenshot(path=out, type="jpeg", quality=90); await ctx.close(); print(out)
        await br.close()
asyncio.run(main())
