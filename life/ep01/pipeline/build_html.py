#!/usr/bin/env python3
"""Build per-platform/per-device video HTML (player + render frame mode) from timeline.json.
usage: build_html.py <lang> <kind:long|shorts|feed> <timeline.json> <out_dir> <render|publish>"""
import json, sys, os, re, html
sys.path.insert(0, os.path.dirname(__file__))
from tts import split_sentences
from locale_text import L  # per-language strings

RAW = "https://raw.githubusercontent.com/soulthread88/{repo}/main/life/ep01/{path}"
FMT = {  # kind -> device -> geometry
    "long":   {"pc": dict(W=3840, H=2160, FS=118, SX=200, SR=200, SB=150, ST=130),
               "mobile": dict(W=3840, H=2160, FS=150, SX=280, SR=280, SB=340, ST=230)},
    "shorts": {"pc": dict(W=2160, H=3840, FS=120, SX=150, SR=150, SB=620, ST=240),
               "mobile": dict(W=2160, H=3840, FS=128, SX=140, SR=380, SB=1060, ST=340)},
    "feed":   {"all": dict(W=2160, H=2700, FS=112, SX=150, SR=150, SB=170, ST=150)},
}
PLATFORM = {"long": "longform-facebook-x", "shorts": "shorts-reels-tiktok", "feed": "threads-instagram-feed"}
METER = {"hook": 8, "intro": 10, "goguma": 45, "turning": 75, "saida": 92, "ending": 100}


def cues_from(tl, lang):
    out = []
    for si, s in enumerate(tl["scenes"]):
        for p in s["paras"]:
            sents = split_sentences(p["text"], lang)
            # merge very short fragments
            merged = []
            for x in sents:
                if merged and len(merged[-1]) < (10 if lang != "en" else 24):
                    merged[-1] += " " + x
                else:
                    merged.append(x)
            tot = sum(len(x) for x in merged) or 1
            a, d = p["start"], p["end"] - p["start"]
            for x in merged:
                b = a + d * len(x) / tot
                out.append(dict(a=round(a, 3), b=round(b, 3), text=x, s=si))
                a = b
    # extend each cue to next cue start (no blank gaps)
    for i in range(len(out) - 1):
        out[i]["b"] = out[i + 1]["a"]
    out[-1]["b"] = tl["duration"] + 3
    return out


def thumb_html(kind, g, t):
    W, H = g["W"], g["H"]
    land = W > H
    u = W / 3840 if land else W / 2160
    def px(v): return f"{v*u:.0f}px"
    bgkey = t.get("bg", "korean_restaurant")
    parts = [f'<div class="bg" data-thumbbg="{bgkey}"></div><div class="th-shade" style="{"" if land else "background:linear-gradient(180deg,rgba(255,250,240,.95) 0%,rgba(255,250,240,.7) 45%,rgba(255,250,240,.2) 75%)"}"></div>']
    if land:
        parts += [f'<div class="th-badge" style="left:{px(200)};top:{px(170)};font-size:{px(118)}">{t["badge"]}</div>',
                  f'<div class="th-big" style="left:{px(200)};top:{px(400)};font-size:{px(330)}">{t["big1"]}<br><b>{t["big2"]}</b></div>',
                  f'<div class="th-q villain" style="left:{px(200)};bottom:{px(200)};font-size:{px(96)};max-width:{px(1700)}"><small>{t["vlabel"]}</small>“{t["villain"]}”</div>',
                  f'<div class="th-q hero" style="right:{px(200)};bottom:{px(200)};font-size:{px(104)};max-width:{px(1600)}"><small>{t["hlabel"]}</small>“{t["hero"]}”</div>',
                  f'<div class="th-tag" style="right:{px(200)};top:{px(170)};font-size:{px(72)}">{t["tag"]}</div>']
    else:
        top = 300 if kind == "shorts" else 160
        side = 150
        big = 300 if len(t["big2"]) <= 8 else 220
        parts += [f'<div style="position:absolute;left:{px(side)};right:{px(side)};top:{px(top)};display:flex;flex-direction:column;align-items:flex-start;gap:{px(60)}">'
                  f'<div class="th-tag" style="position:static;font-size:{px(70)}">{t["tag"]}</div>'
                  f'<div class="th-badge" style="position:static;font-size:{px(112)}">{t["badge"]}</div>'
                  f'<div class="th-big" style="position:static;font-size:{px(big)}">{t["big1"]}<br><b>{t["big2"]}</b></div>'
                  f'<div class="th-q villain" style="position:static;font-size:{px(96)};max-width:{px(1700)}"><small>{t["vlabel"]}</small>“{t["villain"]}”</div>'
                  f'<div class="th-q hero" style="position:static;align-self:flex-end;font-size:{px(104)};max-width:{px(1750)}"><small>{t["hlabel"]}</small>“{t["hero"]}”</div></div>']
    return "\n".join(parts)


def main(lang, kind, tlpath, outdir, target):
    tl = json.load(open(tlpath))
    t = L[lang]
    man = json.load(open(os.path.join(os.path.dirname(__file__), "..", "build", "stock", "manifest.json")))
    tpl = open(os.path.join(os.path.dirname(__file__), "player_template.html"), encoding="utf-8").read()
    cues = cues_from(tl, lang)
    os.makedirs(outdir, exist_ok=True)
    made = []
    for dev, g in FMT[kind].items():
        land = g["W"] > g["H"]
        orient = "landscape" if land else "portrait"
        keys = sorted({s["bg"] for s in tl["scenes"]} | {t["thumb"].get("bg", "korean_restaurant")})
        if target == "render":
            imgs = {k: os.path.abspath(f"build/web/img/{k}_{orient}.jpg") for k in keys}
            vids, audio = {}, ""
        else:
            imgs = {k: RAW.format(repo="imgs", path=f"{k}_{orient}.jpg") for k in keys}
            vids = {k: RAW.format(repo="videos", path=f"broll/{k}_{orient}.mp4") for k in keys
                    if f"{k}_{orient}.mp4" in man}
            audio = RAW.format(repo="audio", path=f"{lang}/lifestory-ep01-{kind}-{lang}.mp3")
        data = dict(lang=lang, W=g["W"], H=g["H"], mode="view", cues=cues,
                    scenes=[dict(title=s["title"], stage=s["stage"], bg=s["bg"]) for s in tl["scenes"]],
                    images=imgs, videos=vids, stageLabels=t["stages"], meter=METER, meterLabel=t["meter"],
                    playLabel=t["play"], pauseLabel=t["pause"])
        tb = t["thumb"].get("bg", "korean_restaurant")
        th = thumb_html(kind, g, t["thumb"]).replace(f'data-thumbbg="{tb}"', f'style="background-image:url(&quot;{imgs[tb]}&quot;)"')
        credits = t["credits_head"] + " " + "; ".join(
            f'{html.escape(v["author"])} ({v["source"]})' for k, v in sorted(man.items())
            if k.split("_landscape")[0].split("_portrait")[0] in keys) + ". " + t["credits_tail"]
        name = f"lifestory-ep01-{PLATFORM[kind]}-{dev}-{lang}.html" if dev != "all" else f"lifestory-ep01-{PLATFORM[kind]}-{lang}.html"
        out = tpl
        for k, v in {"__LANG__": t["htmllang"], "__TITLE__": f'{t["series"]} EP01 · {t["title_short"]} ({PLATFORM[kind]}, {dev})',
                     "__DESC__": t["desc"], "__W__": g["W"], "__H__": g["H"], "__FS__": g["FS"], "__SX__": g["SX"],
                     "__SR__": g["SR"], "__SB__": g["SB"], "__ST__": g["ST"], "__MODE__": "render" if target == "render" else "view", "__ORIENT__": orient,
                     "__BRAND__": f'{t["series"]} · EP01', "__THUMB__": th, "__PLAYLABEL__": t["play"],
                     "__CREDITS__": credits, "__AUDIO__": audio,
                     "__DATA__": json.dumps(data, ensure_ascii=False)}.items():
            out = out.replace(k, str(v))
        p = os.path.join(outdir, name)
        open(p, "w", encoding="utf-8").write(out)
        made.append((p, g, len(cues)))
        print(p, g["W"], g["H"], len(cues), "cues")
    return made


if __name__ == "__main__":
    main(*sys.argv[1:6])
