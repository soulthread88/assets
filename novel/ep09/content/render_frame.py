"""EPIC FURY — 프레임 틀 렌더러 (EP09부터). 사용자가 준 쇼츠 틀을 기준으로 3종 틀을 만든다.
틀: 위 빨간 띠(제목) · 가운데 움직이는 영상(+큰 외곽선 훅 자막) · 아래 빨간 띠(출처 한 줄 + 문장 자막).
  tall 2160x3840 (쇼츠·틱톡·릴스) · feed 2160x2700 (피드·스레드) · wide 3840x2160 (롱폼·X·페이스북)
사용: EF_CONTENT=content_ep09_ko EF_CONTENT_DIR=... EF_MEDIA=... EF_AUDIO=... EF_OUT=... EF_TMP=... python3 render_frame.py PLAT..."""
import os, sys, json, re, html, asyncio, subprocess, importlib
sys.path.insert(0, os.environ.get("EF_CONTENT_DIR", os.getcwd()))
K = importlib.import_module(os.environ["EF_CONTENT"])
L = K.LANG; MEDIA = os.environ["EF_MEDIA"]; AUD = os.environ["EF_AUDIO"]; OUT = os.environ["EF_OUT"]; TMP = os.environ["EF_TMP"]
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
MAN = json.load(open(f"{MEDIA}/manifest.json")); DUR = json.load(open(f"{AUD}/durations.json"))
PG = {p["n"]: p for p in K.PAGES}; FPS = 30; E = html.escape
FONT = {"ko": ("Noto Sans KR", "Noto+Sans+KR"), "en": ("Noto Sans", "Noto+Sans"), "jp": ("Noto Sans JP", "Noto+Sans+JP")}[L]
GF = f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family={FONT[1]}:wght@500;700;900&display=swap'>"
# base CSS size, band geometry (top band height, video bottom y), font sizes
GEO = {"tall": dict(W=1080, H=1920, top=400, vb=1520, title=66, hook=96, sub=66, src=22, brand=26, sublines=3),
       "feed": dict(W=1080, H=1350, top=250, vb=1010, title=56, hook=78, sub=54, src=20, brand=22, sublines=3),
       "wide": dict(W=1920, H=1080, top=170, vb=850, title=58, hook=84, sub=58, src=20, brand=24, sublines=2)}
SRC = {"ko": "출처", "en": "Source", "jp": "出典"}[L]
BRAND = {"ko": "장대한 분노", "en": "EPIC FURY", "jp": "エピック・フューリー"}[L] + f" · EP{K.EP2}"

def credit(key):
    m = MAN[key]
    return f"{SRC}: " + " · ".join(x for x in [m.get("site"), m.get("author"), m.get("license")] if x)

def hl(t):  # {word} -> yellow
    t = E(t).replace("\n", "<br>")
    return re.sub(r"\{(.+?)\}", r"<span class='y'>\1</span>", t)

def css(g):
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{g['W']}px;height:{g['H']}px;background:transparent;font-family:'{FONT[0]}',sans-serif;overflow:hidden}}
.band{{position:absolute;left:0;right:0;background:repeating-linear-gradient(135deg,#e8000f 0 14px,#de000e 14px 28px);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 40px}}
.top{{top:0;height:{g['top']}px;border-bottom:7px solid #9d0009}}
.bot{{top:{g['vb']}px;bottom:0;border-top:7px solid #9d0009;justify-content:flex-start;padding-top:12px}}
.o{{color:#fff;font-weight:900;-webkit-text-stroke:{max(6, g['title']//8)}px #000;paint-order:stroke fill;line-height:1.22;word-break:keep-all;overflow-wrap:anywhere}}
.y{{color:#ffd400}}
.brand{{position:absolute;top:12px;left:20px;color:#ffd400;font-weight:900;font-size:{g['brand']}px;-webkit-text-stroke:4px #000;paint-order:stroke fill}}
.title{{font-size:{g['title']}px;max-width:100%}}
.hook{{position:absolute;left:30px;right:30px;top:{g['top']}px;height:{g['vb']-g['top']}px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:{int((g['vb']-g['top'])*0.10)}px;text-align:center}}
.hook .o{{font-size:{g['hook']}px;-webkit-text-stroke:{g['hook']//7}px #000;line-height:1.18;text-shadow:0 6px 18px rgba(0,0,0,.45)}}
.src{{font-size:{g['src']}px;font-style:italic;font-weight:700;color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke fill;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;margin-bottom:10px}}
.badge{{display:inline-block;font-weight:900;font-size:{g['title']*0.55:.0f}px;padding:.1em .5em;margin:0 .25em;border-radius:8px}}
.b1{{background:#ffd400;color:#000}} .b2{{background:#000;color:#fff}}
"""

def base_html(g, top, hook, key, bottom_extra=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{css(g)}</style></head><body>"
            f"<div class='band top'><div class='brand'>{E(BRAND)}</div><div class='o title' id='TT'>{hl(top)}</div></div>"
            f"<div class='hook'><div class='o' id='HK'>{hl(hook)}</div></div>"
            f"<div class='band bot'><div class='src'>{E(credit(key))}</div>{bottom_extra}</div></body></html>")

def sub_html(g, text):
    h = g["H"] - g["vb"]
    return (f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{css(g)} html,body{{height:{h}px}}"
            f".s{{position:absolute;left:30px;right:30px;top:{g['src']+30}px;bottom:14px;display:flex;align-items:center;justify-content:center;text-align:center}}"
            f".s .o{{font-size:{g['sub']}px}}</style></head><body><div class='s'><div class='o' id='SB'>{hl(text)}</div></div></body></html>")

FIT = """([id,maxH,minF])=>{const e=document.getElementById(id);if(!e)return;let f=parseFloat(getComputedStyle(e).fontSize);
 const box=e.parentElement; while((e.scrollHeight>maxH||e.scrollWidth>box.clientWidth+2)&&f>minF){f-=2;e.style.fontSize=f+'px';e.style.webkitTextStrokeWidth=Math.max(4,f/8)+'px';}}"""

def sentences(t):
    t = re.sub(r"\s+", " ", t.replace("\n", " ")).strip()
    parts = re.findall(r'.+?(?:[.?!]+["”」』]*(?=\s|$)|[。？！]+[」』]*|」(?=「))|.+?$', t)
    parts = [p.strip() for p in parts if p.strip()]
    out = []
    for p in parts:
        if out and (len(out[-1]) < (14 if L != "en" else 26) or p in ('"', '”', '」')): out[-1] += ("" if L == "jp" else " ") + p
        else: out.append(p)
    lim = {"ko": 72, "jp": 66, "en": 135}[L]
    res = []
    for p in out:
        while len(p) > lim:
            cands = [p.rfind(x, 0, lim) for x in (", ", "、", "，")]
            cut = max(cands)
            if cut < lim * 0.35: cut = p.rfind(" ", 0, lim)
            if cut < lim * 0.35: cut = lim
            head, tail = p[:cut + 1].strip(), p[cut + 1:].strip()
            if len(tail) < lim * 0.3: break
            res.append(head); p = tail
        if p: res.append(p)
    return res

async def render_pngs(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch()
        ctxs = {}
        for j in jobs:
            if os.path.exists(j["png"]): continue
            key = (j["vw"], j["vh"], j["dpr"])
            if key not in ctxs: ctxs[key] = await br.new_context(viewport=dict(width=j["vw"], height=j["vh"]), device_scale_factor=j["dpr"])
            pg = await ctxs[key].new_page()
            await pg.set_content(j["html"], wait_until="networkidle"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(150)
            for fid, mh, mf in j.get("fit", []): await pg.evaluate(FIT, [fid, mh, mf])
            if j.get("hole"):
                from PIL import Image
                await pg.evaluate("()=>{const h=document.querySelector('.hook');h.style.visibility='hidden'}")
                await pg.screenshot(path=j["png"], omit_background=True)
                await pg.evaluate("()=>{document.querySelector('.hook').style.visibility='visible';document.querySelectorAll('.band').forEach(b=>b.style.visibility='hidden')}")
                await pg.screenshot(path=j["png"] + ".hook.png", omit_background=True)
                im = Image.open(j["png"]).convert("RGBA"); x, y, w, h = j["hole"]; im.paste((0, 0, 0, 0), (x, y, x + w, y + h))
                im.alpha_composite(Image.open(j["png"] + ".hook.png").convert("RGBA")); im.save(j["png"]); os.remove(j["png"] + ".hook.png")
            else:
                await pg.screenshot(path=j["png"], omit_background=True)
            await pg.close()
        await br.close()

USE = {}
def media_in(key, D):
    m = MAN[key]; src = f"{MEDIA}/{m['file']}"; vd = float(m.get("duration") or 10)
    USE[key] = USE.get(key, 0) + 1; off = ((USE[key] - 1) * 3.3) % max(vd - 6, 1)
    return ["-stream_loop", "-1", "-ss", f"{off:.2f}", "-t", f"{D + .5:.2f}", "-i", src]

def seg(out, W, H, g, dpr, key, base_png, subs, D):
    vy0, vy1 = round(g["top"] * dpr), round(g["vb"] * dpr); vh = vy1 - vy0; vh -= vh % 2
    ins = media_in(key, D) + ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", base_png]
    fc = [f"color=c=0x101010:s={W}x{H}:r={FPS}:d={D + .5:.2f}[bg]",
          f"[0:v]fps={FPS},setpts=PTS-STARTPTS,scale={int(W * 1.08)}:{int(vh * 1.08)}:force_original_aspect_ratio=increase,"
          f"crop={W}:{vh}:x='(iw-{W})/2+(iw-{W})/2*sin(t/{D:.2f}*1.3)*0.7':y='(ih-{vh})/2',eq=brightness=0.04:contrast=1.04:saturation=1.1[v]",
          f"[bg][v]overlay=0:{vy0}:shortest=1[a0]", "[1:v]format=rgba[b]", "[a0][b]overlay=0:0[a1]"]
    last = "[a1]"; idx = 2
    for i, (png, t0, t1) in enumerate(subs):
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", png]
        fc.append(f"[{idx}:v]format=rgba[s{i}]")
        fc.append(f"{last}[s{i}]overlay=0:{vy1}:enable='between(t,{t0:.2f},{t1:.2f})'[a{idx}]"); last = f"[a{idx}]"; idx += 1
    fc.append(f"{last}fade=t=in:st=0:d=0.25,fade=t=out:st={D - 0.25:.2f}:d=0.25,format=yuv420p[vout]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-filter_threads", "2"] + ins + ["-filter_complex", ";".join(fc), "-map", "[vout]", "-t", f"{D:.3f}",
                    "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-maxrate", "26M", "-bufsize", "44M", "-profile:v", "high",
                    "-level", "5.1", "-g", str(FPS * 2), out], check=True)

def pick(plat):
    W, H, pri, lay, ct, cs, cm = K.PLATFORMS[plat]; lo, hi = K.SPECS[plat][3], K.SPECS[plat][4]
    tail = 1.0 if plat == "longform" else 0.6
    fixed = DUR["cover_" + plat]["dur"] + 1.5 + DUR["end"]["dur"] + 1.5
    d = lambda n: DUR[f"p{n:02d}"]["dur"] + 0.5 + tail
    if plat == "longform":
        sel = list(range(1, len(K.PAGES) + 1)); tot = fixed + sum(d(n) for n in sel)
        if tot < lo: tail += (lo - tot) / len(sel) + 0.05
        return sel, tail
    sel, tot = [], fixed
    for n in pri + [x for x in range(1, len(K.PAGES) + 1) if x not in pri]:
        if tot >= lo: break
        if tot + d(n) <= hi: sel.append(n); tot += d(n)
    return sorted(sel), tail

def build(plat):
    W, H, pri, lay, ctitle, csub, cmedia = K.PLATFORMS[plat]; g = GEO[lay]; dpr = W / g["W"]
    picks, tail = pick(plat); wd = f"{TMP}/{plat}"; os.makedirs(wd, exist_ok=True)
    seq = [dict(kind="cover", key="cover_" + plat, top=f"{K.X['series']}", hook="{" + ctitle + "}", media=cmedia,
                extra=f"<div class='o title'><span class='badge b1'>{K.X['fiction']}</span><span class='badge b2'>{K.X['badge']}</span> {E(csub)}</div>")]
    seq += [dict(kind="page", key=f"p{n:02d}", top=PG[n]["top"], hook=PG[n]["hook"], media=PG[n]["media"], text=PG[n]["text"], end=PG[n].get("end")) for n in picks]
    seq += [dict(kind="cover", key="end", top=K.X["title"], hook="{" + K.END_TITLE + "}", media=K.END_MEDIA,
                 extra=f"<div class='o title'>{E(K.END_SUB)}</div>")]
    jobs, plan = [], []
    hole = (0, round(g["top"] * dpr), W, round((g["vb"] - g["top"]) * dpr))
    for i, s in enumerate(seq):
        bp = f"{wd}/s{i:02d}_base.png"
        jobs.append(dict(png=bp, vw=g["W"], vh=g["H"], dpr=dpr, hole=hole, html=base_html(g, s["top"], s["hook"], s["media"], s.get("extra", "")),
                         fit=[["TT", g["top"] - 50, 24], ["HK", (g["vb"] - g["top"]) * 0.8, 30]]))
        a = DUR[s["key"]]["dur"]; lead = 0.5
        D = lead + a + (tail if s["kind"] == "page" else 1.5)
        subs = []
        if s["kind"] == "page":
            ss = sentences(s["text"]) + ([K.END_NOTE] if s.get("end") else [])
            tot = sum(len(x) for x in ss[:len(sentences(s["text"]))]); t = lead
            for k, x in enumerate(ss):
                dt = a * len(x) / tot if k < len(sentences(s["text"])) else (D - t - 0.2)
                sp = f"{wd}/s{i:02d}_sub{k:02d}.png"
                jobs.append(dict(png=sp, vw=g["W"], vh=g["H"] - g["vb"], dpr=dpr, html=sub_html(g, x), fit=[["SB", (g["H"] - g["vb"]) - g["src"] - 60, 24]]))
                subs.append([sp, max(0, t - 0.15), None, x]); t += dt
            for k in range(len(subs)): subs[k][2] = (subs[k + 1][1] - 0.04) if k < len(subs) - 1 else D
            subs = [tuple(x) for x in subs]
        plan.append((s, bp, subs, D, a))
    asyncio.run(render_pngs(jobs))
    T = 0.0; segs, clips, srt = [], [], []
    for i, (s, bp, subs, D, a) in enumerate(plan):
        out = f"{wd}/s{i:02d}.mp4"
        if not os.path.exists(out): seg(out, W, H, g, dpr, s["media"], bp, [(p, t0, t1) for p, t0, t1, _ in subs], D)
        segs.append(out); clips.append((T + 0.5, f"{AUD}/{DUR[s['key']]['file']}"))
        if subs: srt += [(T + t0, T + t1, x) for _, t0, t1, x in subs]
        else: srt.append((T + 0.3, T + D - 0.2, DUR[s["key"]]["text"]))
        T += D; print(plat, i, s["key"], round(D, 2), flush=True)
    lst = f"{wd}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in segs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", f"{wd}/video.mp4"], check=True)
    ins, fl = [], []
    for k, (st, f) in enumerate(clips):
        ins += ["-i", f]; ms = int(st * 1000); fl.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
    fl.append("".join(f"[a{k}]" for k in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{T:.3f}[aout]")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[aout]", "-ac", "2", "-c:a", "aac", "-b:a", "192k", f"{wd}/narr.m4a"], check=True)
    name = f"epic_fury_ep{K.EP2}_{plat}_{L}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{wd}/video.mp4", "-i", f"{wd}/narr.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy",
                    "-movflags", "+faststart", "-shortest", f"{OUT}/{name}.mp4"], check=True)
    ts = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x - int(x)) * 1000)) % 1000:03d}"
    open(f"{OUT}/{name}.srt", "w").write("\n".join(f"{k + 1}\n{ts(a)} --> {ts(b)}\n{x}\n" for k, (a, b, x) in enumerate(srt)))
    json.dump(dict(picks=picks, tail=tail, dur=round(T, 2)), open(f"{OUT}/{name}.json", "w"))
    print("DONE", name, round(T, 1), picks, flush=True)

if __name__ == "__main__":
    for p in [a for a in sys.argv[1:] if not a.startswith("-")]:
        if "--plan" in sys.argv:
            print(p, pick(p)); continue
        build(p)
