#!/usr/bin/env python3
"""Full-story HTML + platform blog HTMLs. usage: build_pages.py <lang> <outdir>"""
import sys, os, re, json, html, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from locale_text import L

RAW = "https://raw.githubusercontent.com/soulthread88/{repo}/main/life/ep01/{path}"
REL = "https://github.com/soulthread88/videos/releases/download/life-ep01/{name}"
PAGE = {"ko": dict(full="전체 이야기", listen="전체 오디오 듣기", videos="플랫폼별 영상", scene="장면"),
        "en": dict(full="The Full Story", listen="Listen to the full audio drama", videos="Videos by platform", scene="Scene"),
        "jp": dict(full="物語の全文", listen="オーディオドラマを聴く", videos="プラットフォーム別の動画", scene="シーン")}
VIDS = [("longform-facebook-x-pc", "YouTube · Facebook · X (PC)"), ("longform-facebook-x-mobile", "YouTube · Facebook · X (Mobile)"),
        ("shorts-reels-tiktok-pc", "Shorts · Reels · TikTok (PC)"), ("shorts-reels-tiktok-mobile", "Shorts · Reels · TikTok (Mobile)"),
        ("threads-instagram-feed", "Threads · Instagram Feed")]
CSS = """
*{box-sizing:border-box}body{margin:0;background:#fffaf0;color:#1d2a44;font-family:"Noto Sans KR","Noto Sans JP",sans-serif;font-size:21px;line-height:1.85;word-break:keep-all}
.wrap{max-width:860px;margin:0 auto;padding:28px 20px 80px}h1{font-family:"Noto Serif KR","Noto Serif JP",serif;font-size:36px;line-height:1.35;margin:.4em 0}
h2{font-size:28px;margin:1.8em 0 .6em;padding-left:14px;border-left:8px solid #e8573f}h3{font-size:23px;margin:1.4em 0 .4em;color:#e8573f}
img,video{width:100%;border-radius:16px;display:block}figure{margin:1.4em 0}figcaption{font-size:17px;color:#6b5f52;margin-top:6px}
blockquote{margin:1em 0;padding:16px 22px;background:#fff;border-left:8px solid #f4b63a;border-radius:10px;font-weight:700;font-size:23px}
.lead{font-size:23px;font-weight:500}.note{font-size:16px;color:#7a6f62}.tags{color:#3d7be0;font-size:17px}
audio{width:100%;margin:10px 0}.btns{display:flex;flex-wrap:wrap;gap:10px}.btns a{background:#1d2a44;color:#fff;text-decoration:none;padding:10px 16px;border-radius:999px;font-size:17px;font-weight:700}
table{border-collapse:collapse;width:100%;font-size:18px}td,th{border:1px solid #e6dccb;padding:8px 10px;text-align:left}th{background:#f6eedf}
.toc{background:#fff;border-radius:12px;padding:14px 22px;border:2px solid #f0e4cf}.scene p{margin:.5em 0}
.badge{display:inline-block;background:#e8573f;color:#fff;font-weight:900;border-radius:8px;padding:2px 12px;font-size:16px}
"""
HEAD = """<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:image" content="{og}">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Sans+JP:wght@400;700;900&family=Noto+Serif+KR:wght@700;900&family=Noto+Serif+JP:wght@700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body><div class="wrap">"""


def media(lang):
    aud = RAW.format(repo="audio", path=f"{lang}/lifestory-ep01-long-{lang}.mp3")
    v = REL.format(name=f"lifestory-ep01-longform-facebook-x-pc-{lang}.mp4")
    thumb = RAW.format(repo="imgs", path=f"thumb/lifestory-ep01-thumb-landscape-{lang}.jpg")
    return aud, v, thumb


def main(lang, outdir):
    os.makedirs(outdir, exist_ok=True)
    t, P = L[lang], PAGE[lang]
    aud, vid, thumb = media(lang)
    img = lambda k: RAW.format(repo="imgs", path=f"{k}_landscape.jpg")
    video_tag = f'<figure><video controls preload="none" poster="{thumb}" src="{vid}"></video></figure>'
    audio_tag = f'<audio controls preload="none" src="{aud}"></audio>'
    # blogs
    spec = importlib.util.spec_from_file_location("b", f"ep01/{lang}/blogs.py")
    b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
    for plat, d in b.BLOGS.items():
        body = d["body"].replace("{VIDEO}", video_tag).replace("{AUDIO}", audio_tag)
        body = re.sub(r"\{IMG:(\w+)\}", lambda m: img(m[1]), body)
        page = HEAD.format(lang=t["htmllang"], title=html.escape(d["title"]), desc=html.escape(t["desc"]), og=thumb, css=CSS)
        page += f'<span class="badge">{t["series"]} EP01 · {plat.capitalize()}</span><h1>{html.escape(d["title"])}</h1>'
        page += f'<figure><img src="{thumb}" alt="{html.escape(d["title"])}"></figure>' + body
        page += f'<p class="tags">{html.escape(d["tags"])}</p></div></body></html>'
        open(f"{outdir}/lifestory-ep01-blog-{plat}-{lang}.html", "w", encoding="utf-8").write(page)
    # full story
    tl = json.load(open(f"build/{lang}/long/timeline.json"))
    page = HEAD.format(lang=t["htmllang"], title=f'{t["series"]} EP01 · {html.escape(t["title_short"])}', desc=html.escape(t["desc"]), og=thumb, css=CSS)
    page += f'<span class="badge">{t["series"]} EP01</span><h1>{html.escape(t["title_short"])}</h1><figure><img src="{thumb}" alt=""></figure>'
    page += f'<p class="lead">{html.escape(t["desc"])}</p><h2>{P["listen"]}</h2>{audio_tag}<h2>{P["videos"]}</h2><div class="btns">'
    for slug, label in VIDS:
        page += f'<a href="{REL.format(name=f"lifestory-ep01-{slug}-{lang}.mp4")}">{label}</a>'
    page += f'</div><h2>{P["full"]}</h2>'
    for i, s in enumerate(tl["scenes"]):
        page += f'<section class="scene"><h3>{i+1}. {html.escape(s["title"])}</h3>'
        if i % 3 == 0:
            page += f'<figure><img loading="lazy" src="{img(s["bg"])}" alt=""></figure>'
        page += "".join(f"<p>{html.escape(p['text'])}</p>" for p in s["paras"]) + "</section>"
    page += f'<p class="note">{t["credits_head"]} {t["credits_tail"]}</p></div></body></html>'
    open(f"{outdir}/lifestory-ep01-full-{lang}.html", "w", encoding="utf-8").write(page)
    print("pages ok", lang)


if __name__ == "__main__":
    main(*sys.argv[1:3])
