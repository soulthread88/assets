# -*- coding: utf-8 -*-
"""EP10 블로그 생성(GEO). Naver·Tistory=KO, WordPress·Substack=KO+EN.
이미지 = 각 장면 4K 영상의 정지 화면(출처는 원 영상), 영상 = 플랫폼 MP4 링크/임베드."""
import json, html, re, os, sys
E = html.escape
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/blog"; os.makedirs(OUT, exist_ok=True)
MAN = json.load(open("/home/claude/work/media_ep10/manifest.json"))
IMG = "https://raw.githubusercontent.com/soulthread88/imgs/main/novel/ep10/"
VID = "https://media.githubusercontent.com/media/soulthread88/videos/main/novel/ep10/platform_{L}/"
POSTED = "2026-11-15"; PLATS = ["longform", "shorts", "threads", "x"]
sys.path.insert(0, D)
from blog_t10 import T
SCENE_KEY = ["vid_sea_strait", "vid_monitors", "vid10_pomegranate", "vid9_p11", "vid10_atlas", "vid10_tanker", "vid10_radio"]  # 장면별 정지 화면(원 영상 출처)

def lines(L): return [x.strip() for x in open(f"/home/claude/work/ep10_{L}.txt").read().splitlines()]
def section(L, start, n):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == start)
    return ls[i + 1:i + 1 + n]
def notes(L, t):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == t["notes"]); j = next(k for k, x in enumerate(ls) if x.strip() == t["nxt"])
    blk = ls[i + 1:j]
    TY = r"(실존 인물|실존 사건|실존 발언|가상 인물|역사|국제 조약|Real person|Real events|Real statement|Fictional character|History|International treaty)"
    return [(re.sub(r"\s*" + TY, r" — \1", blk[k], count=1), blk[k + 1]) for k in range(0, len(blk) - 1, 2)]
def chars(L, t):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == t["chars"]); j = next(k for k, x in enumerate(ls) if x.strip() == t["notes"])
    blk = ls[i + 2:j]; return [(blk[k], blk[k + 1], blk[k + 4]) for k in range(0, len(blk) - 4, 5)]
def sources(L, t):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == t["src"])
    out = []
    for x in ls[i + 1:]:
        m = re.search(r"(https?://\S+?)(https?://\S+)?$", x)
        if m and not x.startswith(("이미지", "Image", "장면 요약", "Scene summary", "영상", "Video")): out.append((x[:m.start()].strip(), m.group(1)))
    return out
def img_key(i): return SCENE_KEY[i]
def img_url(k): return IMG + k + ".jpg"
def credit(k, t):
    m = MAN[k]; return " · ".join(x for x in [m.get("author"), m.get("license"), m.get("site")] if x)

def build(L, mode):
    t = T[L]; SC = json.load(open(f"{D}/scenes_{L}.json")); H = []
    st = (lambda k: f' style="{k}"') if mode == "naver" else (lambda k: "")
    S = dict(h1="font-size:32px;line-height:1.35;font-weight:900;color:#0b2245;margin:0 0 12px",
             h2="font-size:26px;line-height:1.4;font-weight:800;color:#0b2245;margin:44px 0 14px;padding-left:14px;border-left:8px solid #e8000f",
             h3="font-size:21px;font-weight:800;color:#c8202d;margin:24px 0 8px", p="margin:0 0 18px",
             cap="font-size:16px;margin:8px 0 2px;font-weight:500", src="font-size:14px;font-style:italic;color:#555;margin:0",
             td="padding:10px;border:1px solid #e3dccb;vertical-align:top", th="background:#0b2245;color:#fff;padding:10px;text-align:left")
    h = lambda tag, x: f"<{tag}{st(S[tag])}>{x}</{tag}>"
    p = lambda x, cls="": (f'<p class="{cls}">{E(x)}</p>' if cls and mode in ("wordpress", "tistory") else f"<p{st(S['p'])}>{E(x)}</p>")
    def fig(k, cap, video=None):
        m = MAN[k]
        if mode == "substack": return f'<figure><img src="{img_url(k)}" alt="{E(cap)}"><figcaption>{E(cap)} — {t["srcw"]}: <a href="{E(m["page"])}">{E(credit(k, t))}</a></figcaption></figure>'
        if mode == "naver": return (f'<p style="margin:22px 0 4px"><img src="{img_url(k)}" alt="{E(cap)}" style="width:100%;height:auto"></p><p style="{S["cap"]}">{E(cap)}</p>'
                                    f'<p style="{S["src"]}"><i>{t["srcw"]}: <a href="{E(m["page"])}" style="color:#555">{E(credit(k, t))}</a></i></p>')
        media = (f'<video controls preload="metadata" poster="{img_url(k)}" src="{video}"></video>' if video else f'<img src="{img_url(k)}" alt="{E(cap)}" width="3840" height="2160" loading="lazy">')
        return f'<figure>{media}<figcaption><p class="cap">{E(cap)}</p><p class="src"><i>{t["srcw"]}: <a href="{E(m["page"])}" target="_blank" rel="noopener">{E(credit(k, t))}</a></i></p></figcaption></figure>'
    H.append(h("h1", E(t["title"])))
    H.append(f'<p class="meta"{st("font-size:16px;color:#555;margin:0 0 20px")}>{E(t["meta"])} · {POSTED}</p>')
    H.append(fig("img_lincoln10", t["tldr"][0][:60] + "…"))
    li = "".join(f"<li>{E(x)}</li>" for x in t["tldr"])
    H.append(f'<div class="tldr"{st("background:#fff4f4;border:2px solid #e8000f;border-radius:10px;padding:18px 24px;margin:18px 0 28px")}><strong>{E(t["tldr_h"])}</strong><ul>{li}</ul></div>'
             if mode != "substack" else f"{h('h2', E(t['tldr_h']))}<ul>{li}</ul>")
    H.append(h("h2", E(t["num_h"])))
    if mode == "substack": H.append("<ul>" + "".join(f"<li><strong>{E(a)}: {E(b)}</strong> — {E(c)}</li>" for a, b, c in t["nums"]) + "</ul>")
    else:
        H.append(f'<table{st("width:100%;border-collapse:collapse;font-size:17px")}><thead><tr>' + "".join(f"<th{st(S['th'])}>{E(c)}</th>" for c in t["num_cols"]) + "</tr></thead><tbody>" +
                 "".join(f"<tr><td{st(S['td'])}>{E(a)}</td><td{st(S['td'])}><b{st('color:#c8202d;font-size:21px')}>{E(b)}</b></td><td{st(S['td'])}>{E(c)}</td></tr>" for a, b, c in t["nums"]) + "</tbody></table>")
    H.append(h("h2", E(t["tl_h"])))
    for a, b in t["tl"]: H.append(h("h3", E(a)) + p(b))
    H.append(fig("img_army10", t["tl"][1][1]))
    H.append(h("h2", E(t["vid_h"])))
    V = VID.format(L=L)
    if mode in ("wordpress", "tistory"): H.append(fig("img_lincoln10", t["vid_names"]["longform"], video=V + f"epic_fury_ep10_longform_{L}.mp4"))
    links = [(t["vid_names"][k], V + f"epic_fury_ep10_{k}_{L}.mp4") for k in PLATS]
    H.append("<ul>" + "".join(f'<li><a href="{u}">{E(n)}</a></li>' for n, u in links) + "</ul>")
    H.append(h("h2", E(t["body_h"])))
    for i, sc in enumerate(SC):
        paras = sc["paras"]
        paras = [(c, re.sub(r"\s*✦\s*(공유|Share)\s*$", "", x)) for c, x in paras]
        H.append(h("h2", f"{t['scene']} {i + 1}. {E(t['q'][i])}"))
        intro = f'<p{st("font-weight:800;color:#0b2245;margin:0 0 4px")} class="place"><b>{E(sc["place"])}</b></p><p{st("font-size:15px;color:#555;margin:0 0 14px")} class="time"><i>{E(sc["time"])}</i></p>'
        cls = lambda c: {"dialogue": "dlg", "factual": "fact", "impact": "impact", "shareable": "impact"}.get(c, "")
        body = "".join((f"<blockquote>{E(x)}</blockquote>" if mode == "substack" and c in ("impact", "shareable") else p(x, cls(c))) for c, x in paras)
        f = fig(img_key(i), sc["place"])
        if mode in ("wordpress", "tistory"):
            first = "".join(p(x, cls(c)) for c, x in paras[:2]); rest = "".join(p(x, cls(c)) for c, x in paras[2:])
            H.append(f'<div class="row"><div class="col">{intro}{first}</div>{f}</div>{rest}')
        else: H.append(intro + f + body)
    H.append(p(t["end"]))
    H.append(h("h2", E(t["dip_h"])) + "".join(p(x) for x in t["dip"]))
    b = section(L, t["bg"], 4)
    H.append(h("h2", E(t["bg_h"])) + "".join(p(x) for x in b[1:]))
    H.append(h("h2", E(t["fact_h"])))
    for a, x in notes(L, t): H.append(h("h3", E(a)) + p(x))
    H.append(h("h2", E(t["char_h"])))
    H.append("".join(p(f"■ {a} ({b}) — {c}") for a, b, c in chars(L, t)))
    H.append(h("h2", E(t["faq_h"])))
    if mode in ("wordpress", "tistory"): H.append('<dl class="faq">' + "".join(f"<dt>Q. {E(q)}</dt><dd>A. {E(a)}</dd>" for q, a in t["faq"]) + "</dl>")
    else:
        for q, a in t["faq"]: H.append(h("h3", "Q. " + E(q)) + p("A. " + a))
    nx = section(L, t["nxt"], 3)
    H.append(h("h2", E(t["next_h"])) + p(nx[1]) + p(nx[2]))
    H.append(h("h2", E(t["src_h"])))
    items = sources(L, t)
    seen = []
    for k in ["img_lincoln10", "img_army10"] + SCENE_KEY:
        if k in seen: continue
        seen.append(k); m = MAN[k]; items.append((f"{m.get('title') or __import__('urllib.parse').parse.unquote(m['page'].rsplit('File:', 1)[-1]).rsplit('.', 1)[0].replace('_', ' ')} — {credit(k, t)}", m["page"]))
    H.append("<ol>" + "".join(f'<li>{E(a)}<br><a href="{E(u)}" style="word-break:break-all;overflow-wrap:anywhere">{E(u)}</a></li>' for a, u in items) + "</ol>")
    H.append(f'<div class="disc"{st("font-size:15px;color:#555;background:#f6f3ec;padding:14px 18px;border-radius:8px;margin:24px 0")}>{E(t["disc"])}</div>' if mode != "substack" else f"<p><em>{E(t['disc'])}</em></p>")
    if mode in ("naver", "tistory"): H.append(f'<p{st("color:#555;font-size:16px")}>' + " ".join("#" + x for x in t["tags"]) + "</p>")
    body = "\n".join(H)
    if mode == "substack": return body
    if mode == "naver": return f'<div style="font-family:\'Noto Sans KR\',\'Malgun Gothic\',sans-serif;color:#141414;font-size:19px;line-height:1.9;word-break:keep-all;max-width:860px;margin:0 auto">\n{body}\n</div>'
    fam = "'Noto Sans KR'" if L == "ko" else "'Noto Sans'"
    css = f"""
.efb{{font-family:{fam},sans-serif;color:#141414;font-size:19px;line-height:1.9;word-break:keep-all;max-width:880px;margin:0 auto}}
.efb h1{{{S['h1']}}} .efb h2{{{S['h2']}}} .efb h3{{{S['h3']}}} .efb p{{{S['p']}}} .efb .meta{{font-size:16px;color:#555}}
.efb .tldr{{background:#fff4f4;border:2px solid #e8000f;border-radius:10px;padding:18px 24px;margin:18px 0 28px}} .efb .tldr ul{{margin:8px 0 0;padding-left:22px}}
.efb figure{{margin:22px 0 26px}} .efb figure img,.efb figure video{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:8px}}
.efb .cap{{{S['cap']}}} .efb .src{{{S['src']}}} .efb .src a{{color:#555}}
.efb table{{width:100%;border-collapse:collapse;margin:10px 0 24px;font-size:17px}} .efb th{{{S['th']}}} .efb td{{{S['td']}}}
.efb .row{{display:flex;gap:28px;align-items:center;flex-wrap:wrap;margin:18px 0 8px}} .efb .row .col{{flex:1 1 380px;min-width:0}} .efb .row figure{{flex:1 1 380px;margin:0}}
.efb .place{{font-size:17px}} .efb .time{{font-size:15px;color:#555}} .efb .dlg{{padding-left:14px;border-left:3px solid #e3dccb}}
.efb .fact{{background:#f6f3ec;padding:12px 16px;border-radius:8px;font-size:17px}} .efb .impact{{font-weight:800;color:#c8202d}}
.efb .faq dt{{font-weight:800;color:#0b2245;margin-top:16px}} .efb .faq dd{{margin:6px 0 0}} .efb .disc{{font-size:15px;color:#555;background:#f6f3ec;padding:14px 18px;border-radius:8px}}
@media (max-width:640px){{.efb{{font-size:18px}} .efb h1{{font-size:26px}} .efb h2{{font-size:22px}}}}"""
    fq = "Noto+Sans+KR" if L == "ko" else "Noto+Sans"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": t["title"][:110], "description": t["desc"], "inLanguage": L, "datePublished": POSTED, "dateModified": POSTED, "genre": "War fiction",
         "keywords": ", ".join(t["kw"]), "image": [img_url("img_lincoln10")], "author": {"@type": "Organization", "name": "Epic Fury · SOULTHREAD"},
         "isPartOf": {"@type": "CreativeWorkSeries", "name": "Epic Fury: Night Over Hormuz"},
         "about": [{"@type": "Thing", "name": "2026 Iran war"}, {"@type": "Place", "name": "Islamabad"}, {"@type": "Place", "name": "Kuwait International Airport"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@type": "VideoObject", "name": t["vid_names"]["longform"] + " — " + t["title"][:60], "description": t["desc"], "thumbnailUrl": img_url("img_lincoln10"),
         "uploadDate": POSTED, "contentUrl": V + f"epic_fury_ep10_longform_{L}.mp4", "inLanguage": L}]}
    return (f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fq}:wght@400;500;700;800;900&display=swap"><style>{css}</style>\n'
            f'<div class="efb">\n{body}\n</div>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

def page(L, mode, b):
    t = T[L]; fq = "Noto+Sans+KR" if L == "ko" else "Noto+Sans"
    extra = "" if mode in ("wordpress", "tistory") else f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family={fq}:wght@400;700;900&display=swap'><style>body{{font-family:'Noto Sans KR','Noto Sans',sans-serif;font-size:19px;line-height:1.9;max-width:860px;margin:0 auto;padding:16px}} img{{max-width:100%;height:auto}}</style>"
    return (f"<!doctype html><html lang='{L}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{E(t['title'])}</title>"
            f"<meta name='description' content='{E(t['desc'])}'><meta name='keywords' content='{E(', '.join(t['kw']))}'><meta property='og:title' content='{E(t['title'])}'>"
            f"<meta property='og:description' content='{E(t['desc'])}'><meta property='og:image' content='{img_url('img_lincoln10')}'><meta property='og:type' content='article'>{extra}</head>"
            f"<body style='background:#fbf9f4;margin:0;padding:16px'>{b}</body></html>")

if __name__ == "__main__":
    for L, mode in [("ko", "naver"), ("ko", "tistory"), ("ko", "wordpress"), ("ko", "substack"), ("en", "wordpress"), ("en", "substack")]:
        b = build(L, mode); base = f"{OUT}/epic_fury_ep10_blog_{mode}_{L}"
        open(base + ".html", "w").write(page(L, mode, b)); open(base + "_body.html", "w").write(b); print(L, mode, len(b))
