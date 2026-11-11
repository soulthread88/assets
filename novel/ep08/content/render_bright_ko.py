"""EPIC FURY — 밝은 화면 · 시니어 가독성 판 렌더러 (KO). EP08부터.
- 모든 글자는 Noto Sans KR. 본문은 밝은 바탕 위 짙은 글씨(고대비), 글자 크게.
- 이미지/영상은 어둡게 덧칠하지 않고 밝게(eq 밝기·채도 소폭 상향). 박스 바로 아래 줄에 출처.
- wide(16:9): 왼쪽 글 칼럼 + 오른쪽 16:9 미디어 박스(글 칼럼 세로 중앙). band(9:16, 4:5): 위 미디어 박스 + 출처 + 아래 글.
환경변수는 render_v3_ko.py와 같다(EF_CONTENT, EF_CONTENT_DIR, EF_MEDIA, EF_AUDIO, EF_OUT, EF_TMP)."""
import os, sys, json, subprocess, html, asyncio, importlib
sys.path.insert(0, os.environ.get('EF_CONTENT_DIR', os.getcwd()))
K = importlib.import_module(os.environ.get('EF_CONTENT', 'content_epXX_ko'))
ROOT = os.environ.get("EF_ROOT", os.getcwd()); MEDIA = os.environ.get("EF_MEDIA", f"{ROOT}/media")
AUD = os.environ.get("EF_AUDIO", f"{ROOT}/audio_ko"); OUT = os.environ.get("EF_OUT", f"{ROOT}/out_ko"); TMP = os.environ.get("EF_TMP", f"{ROOT}/tmp_ko")
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
MAN = json.load(open(f"{MEDIA}/manifest.json")); DUR = json.load(open(f"{AUD}/durations.json"))
FPS = 30; E = html.escape; PG = {p["n"]: p for p in K.PAGES}; NPAGES = len(K.PAGES)
BG = "f5f2ea"
GF = "<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap'>"

def credit(key):
    m = MAN[key]
    if m.get("site", "").startswith("AI"):
        return f"출처: {m['site']}"
    parts = [m.get("site", ""), m.get("author", ""), m.get("license", "")]
    return "출처: " + " · ".join(p for p in parts if p)

BASE = f"""
:root{{--navy:#0b2245;--gold:#f2b21b;--ink:#141414;--sub:#4a4a4a;--red:#c8202d;--bg:#{BG}}}
*{{box-sizing:border-box;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
html,body{{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans KR","Noto Sans CJK KR",sans-serif;overflow:hidden}}
.header{{display:grid;grid-template-columns:32% 36% 32%;align-items:center;background:var(--navy);color:#fff;border-bottom:4px solid var(--gold)}}
.brand-left{{font-weight:800;color:var(--gold)}}
.logo{{display:flex;flex-direction:column;align-items:center;line-height:1.15}}
.logo .l1{{font-weight:900}} .logo .l2{{font-weight:700;color:var(--gold)}}
.datetime{{display:flex;justify-content:flex-end;gap:16px;align-items:baseline}}
.datetime .date{{font-weight:800;color:var(--gold)}} .datetime .part{{font-weight:700;color:#fff}}
.box{{position:relative;background:transparent;outline:3px solid #fff;box-shadow:0 6px 22px rgba(0,0,0,.18)}}
.src{{font-style:italic;color:#555;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.tag{{display:inline-block;background:var(--red);color:#fff;font-weight:800;letter-spacing:.03em;border-radius:6px}}
.loc{{color:var(--navy);font-weight:800}}
.scene-tag{{color:var(--navy);font-weight:800}}
.h2{{color:var(--red);font-weight:800}}
.text{{color:var(--ink);font-weight:500;word-break:keep-all;overflow-wrap:break-word}}
.end{{color:var(--red);font-weight:800;margin-top:.6em}}
.breaking{{display:flex;align-items:center;background:var(--red);color:#fff;white-space:nowrap;overflow:hidden}}
.breaking .bt{{flex:0 0 auto;background:#fff;color:var(--red);font-weight:800;border-radius:6px}}
.breaking .items{{font-weight:700;overflow:hidden;text-overflow:ellipsis}}
.ticker{{display:flex;align-items:center;background:var(--navy);color:#fff;overflow:hidden}}
.ticker .tt{{flex:0 0 auto;color:var(--gold);font-weight:800;border:2px solid var(--gold);border-radius:4px}}
.tw{{flex:1 1 auto;position:relative;height:100%;overflow:hidden}}
"""
WIDE = BASE + """
.stage{position:relative;width:1600px;height:900px}
.header{height:96px;padding:0 50px}
.brand-left{font-size:24px}.logo .l1{font-size:32px}.logo .l2{font-size:20px}.datetime .date{font-size:22px}.datetime .part{font-size:20px}
.body{position:absolute;left:0;right:0;top:96px;display:flex;align-items:center;gap:44px;padding:0 50px 0 50px}
.col{flex:0 0 760px;display:flex;flex-direction:column;justify-content:center}
.media{flex:0 0 700px;display:flex;flex-direction:column;gap:10px}
.box{width:700px;height:394px}
.src{font-size:17px}
.tag{font-size:24px;padding:4px 14px;margin-right:12px}.loc{font-size:24px}
.meta{margin-bottom:18px;display:flex;align-items:center;flex-wrap:wrap;gap:8px}
.scene-tag{font-size:24px}.h2{font-size:32px;margin:6px 0 16px}
.text{font-size:40px;line-height:1.6}
.end{font-size:26px}
.breaking{position:absolute;left:0;right:0;bottom:46px;height:52px;gap:16px;padding:0 50px}
.breaking .bt{font-size:22px;padding:3px 14px}.breaking .items{font-size:23px}
.ticker{position:absolute;left:0;right:0;bottom:0;height:46px;padding:0 0 0 50px;font-size:20px}
.ticker .tt{font-size:19px;padding:2px 12px;margin-right:16px}
"""
BAND = BASE + """
.stage{position:absolute;left:0;width:1080px}
.header{height:104px;padding:0 40px}
.brand-left{font-size:26px}.logo .l1{font-size:34px}.logo .l2{font-size:21px}.datetime .date{font-size:22px}.datetime .part{font-size:22px}
.hl{height:70px;display:flex;align-items:center;justify-content:center;background:#e8e2d3;color:var(--navy);font-size:30px;font-weight:800;border-bottom:2px solid #d7cfbd}
.media{padding:28px 40px 0}
.box{width:1000px;height:563px}
.src{font-size:20px;margin-top:10px}
.col{padding:26px 40px 34px}
.tag{font-size:25px;padding:5px 14px;margin-right:12px}.loc{font-size:25px}
.meta{margin-bottom:16px;display:flex;align-items:center;flex-wrap:wrap;gap:8px}
.scene-tag{font-size:25px}.h2{font-size:34px;margin:6px 0 14px}
.text{font-size:52px;line-height:1.55}
.end{font-size:32px}
.breaking{height:60px;gap:14px;padding:0 40px}
.breaking .bt{font-size:23px;padding:3px 12px}.breaking .items{font-size:22px}
"""
def header(n):
    return (f'<header class="header"><div class="brand-left">{E(K.UI["brand_left"])}</div>'
            f'<div class="logo"><span class="l1">{E(K.UI["l1"])}</span><span class="l2">{E(K.UI["l2"])}</span></div>'
            f'<div class="datetime"><span class="date">{K.DATE}</span><span class="part">{n}/{NPAGES}</span></div></header>')

def text_block(pg):
    if pg["kind"] == "news":
        return (f'<div class="meta"><span class="tag">{E(K.UI["sit"])}</span><span class="loc">{E(pg["loc"])}</span></div>'
                f'<div class="text" id="T">{E(pg["text"])}</div>')
    h2 = f'<div class="h2">{E(pg["h2"])}</div>' if pg.get("h2") else ""
    end = f'<div class="end">{E(K.END_NOTE)}</div>' if pg.get("end") else ""
    return f'<div class="meta"><span class="scene-tag">{E(pg["tag"])}</span></div>{h2}<div class="text" id="T">{E(pg["text"])}</div>{end}'

def page_html(pg, layout, H):
    n = pg["n"]; news = pg["kind"] == "news"
    media = f'<div class="media"><div class="box" id="M"></div><div class="src">{E(credit(pg["media"]))}</div></div>'
    brk = (f'<section class="breaking"><span class="bt">{E(K.UI["breaking"])}</span><span class="items">{E(K.BREAKING[0])}'
           f'&nbsp;&nbsp;|&nbsp;&nbsp;{E(K.BREAKING[1])}</span></section>')
    if layout == "wide":
        bottom = 98 if news else 0
        body = (header(n) + f'<div class="body" style="bottom:{bottom}px"><div class="col" id="C">{text_block(pg)}</div>{media}</div>' +
                ((brk + f'<footer class="ticker"><span class="tt">{E(K.UI["ticker"])}</span><div class="tw" id="TW"></div></footer>') if news else ""))
        return f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{WIDE}</style></head><body><main class='stage'>{body}</main></body></html>"
    hl = f'<div class="hl">{E(K.UI["headline"])}</div>' if news else ""
    body = header(n) + hl + media + f'<div class="col" id="C">{text_block(pg)}</div>' + (brk if news else "")
    return f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{BAND}</style></head><body style='width:1080px;height:{H}px'><main class='stage' id='S'>{body}</main></body></html>"

def cover_html(title, sub, key, wide, H):
    b = 1920 if wide else 1080; s = 1.0 if wide else 1.0
    t = 128 if wide else 88; pad = 90 if wide else 50
    return (f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{BASE}"
            f"html,body{{background:transparent}}"
            f".top{{position:absolute;left:0;right:0;top:0;height:{110 if wide else 120}px;background:var(--navy);border-bottom:5px solid var(--gold);display:flex;align-items:center;justify-content:space-between;padding:0 {pad}px;color:var(--gold);font-weight:800;font-size:{34 if wide else 32}px}}"
            f".panel{{position:absolute;left:0;right:0;bottom:0;background:rgba(255,255,255,.92);padding:{50 if wide else 46}px {pad}px {40 if wide else 46}px;border-top:8px solid var(--gold)}}"
            f".pills span{{display:inline-block;font-weight:900;font-size:{38 if wide else 34}px;padding:.12em .55em;margin-right:.5em;border-radius:6px}}"
            f".pills .a{{background:var(--red);color:#fff}}.pills .b{{background:var(--navy);color:#fff}}"
            f"h1{{margin:.3em 0 0;font-weight:900;font-size:{t}px;line-height:1.14;color:var(--navy);word-break:keep-all}}"
            f".sub{{margin-top:.35em;color:var(--red);font-weight:800;font-size:{48 if wide else 42}px}}"
            f".csrc{{margin-top:18px;font-style:italic;color:#555;font-size:{22 if wide else 22}px}}</style></head>"
            f"<body style='width:{b}px;height:{H}px'><div class='top'><span>{E(K.UI['cover_top'])}</span><span>{E(K.UI['cover_kind'])}</span></div>"
            f"<div class='panel'><div class='pills'><span class='a'>FICTION</span><span class='b'>EP {K.EP2}</span></div>"
            f"<h1>{E(title)}</h1><div class='sub'>{E(sub)}</div><div class='csrc'>{E(credit(key))}</div></div></body></html>")

async def render_layers(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for j in jobs:
            if os.path.exists(j["png"]) and os.path.exists(j["png"] + ".json"): continue
            ctx = await br.new_context(viewport=dict(width=j["vw"], height=j["vh"]), device_scale_factor=j["dpr"])
            pg = await ctx.new_page(); await pg.set_content(j["html"], wait_until='networkidle'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            info = {}
            if j["kind"] == "page":
                if j["layout"] == "band":
                    await pg.evaluate("""(H)=>{const S=document.getElementById('S');const T=document.getElementById('T');
                        let fs=parseFloat(getComputedStyle(T).fontSize);
                        while(S.offsetHeight>H*0.96 && fs>30){fs-=1; T.style.fontSize=fs+'px';}
                        S.style.top=Math.max(0,Math.round(H/2-S.offsetHeight/2))+'px';}""", j["vh"])
                else:
                    await pg.evaluate("""()=>{const C=document.getElementById('C');const B=C.parentElement;const T=document.getElementById('T');
                        let fs=parseFloat(getComputedStyle(T).fontSize);
                        while(C.scrollHeight>B.clientHeight-30 && fs>24){fs-=1; T.style.fontSize=fs+'px';}}""")
                info = await pg.evaluate("""()=>{const r=e=>{if(!e)return null;const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};
                    return {M:r(document.getElementById('M')),TW:r(document.getElementById('TW'))}}""")
            await pg.screenshot(path=j["png"], omit_background=True)
            if info.get("M"):
                from PIL import Image
                im = Image.open(j["png"]).convert("RGBA"); x, y, w, h = [round(v * j["dpr"]) for v in info["M"]]
                im.paste((0, 0, 0, 0), (x, y, x + w, y + h)); im.save(j["png"])
            json.dump({k: ([round(x * j["dpr"]) for x in v] if v else None) for k, v in info.items()}, open(j["png"] + ".json", "w"))
            if j.get("ticker"):
                tk = "".join(f'{E(x)}<span style="margin:0 .8em">|</span>' for x in K.TICKER) * 2
                th = round(info["TW"][3])
                await pg.set_viewport_size(dict(width=8000, height=th))
                await pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'>{GF}<style>{BASE}</style></head><body style='margin:0;height:{th}px;background:#0b2245;"
                                     f"display:flex;align-items:center;white-space:nowrap;font:600 20px \"Noto Sans KR\";color:#fff'><span id=s>{tk}</span></body></html>",
                                     wait_until='networkidle')
                await pg.evaluate('document.fonts.ready')
                w = await pg.evaluate("document.getElementById('s').offsetWidth")
                await pg.set_viewport_size(dict(width=int(w), height=th)); await pg.screenshot(path=j["ticker"])
            await ctx.close()
        await br.close()

USE = {}
def media_input(key, D, alt):
    m = MAN[key]; src = f"{MEDIA}/{m['file']}"
    USE[key] = USE.get(key, 0) + 1
    if m["type"] == "video":
        vd = float(m.get("duration") or 10); off = (3.0 if alt else 0.0) + ((USE[key] - 1) * 2.7) % max(vd - 4, 1)
        return ["-stream_loop", "-1", "-ss", f"{off:.2f}", "-t", f"{D + .5:.2f}", "-i", src], True
    return ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", src], False

BRIGHT = "eq=brightness=0.035:contrast=1.04:saturation=1.08"
def seg(out, W, H, kind, key, png, D, alt=False, ticker=None):
    ins, isvid = media_input(key, D, alt)
    geo = json.load(open(png + ".json"))
    pre = f"fps={FPS},setpts=PTS-STARTPTS," if isvid else ""
    extra = ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", png]
    def fit(w, h, src, lab):
        Z = 1.10
        return (f"{src}scale={int(w*Z)}:{int(h*Z)}:force_original_aspect_ratio=increase,"
                f"crop={w}:{h}:x='(iw-{w})/2+(iw-{w})/2*sin(t/{D:.2f}*1.4)*0.6':y='(ih-{h})/2-(ih-{h})/4*t/{D:.2f}',{BRIGHT}{lab}")
    fc = [f"color=c=0x{BG}:s={W}x{H}:r={FPS}:d={D+.5:.2f}[bg]"]
    if kind == "cover":
        fc.append(fit(W, H, f"[0:v]{pre}", "[box]")); fc.append("[bg][box]overlay=0:0:shortest=1[v0]")
    else:
        x, y, w, h = geo["M"]; w -= w % 2; h -= h % 2
        fc.append(fit(w, h, f"[0:v]{pre}", "[box]")); fc.append(f"[bg][box]overlay={x}:{y}:shortest=1[v0]")
    fc.append("[1:v]format=rgba[ov]"); fc.append("[v0][ov]overlay=0:0[v1]"); last = "[v1]"; idx = 2
    if ticker:
        tx, ty, tw, th = geo["TW"]
        extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", ticker]
        sw = int(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=width", "-of", "csv=p=0", ticker]))
        fc.append(f"[{idx}:v]scale=-1:{th},crop={tw}:{th}:x='mod(t*{int(W/3840*190)}+{(USE.get('_tk',0)*997)%sw},iw/2)':y=0[tk]")
        USE["_tk"] = USE.get("_tk", 0) + 1
        fc.append(f"{last}[tk]overlay={tx}:{ty}[v2]"); last = "[v2]"
    fc.append(f"{last}fade=t=in:st=0:d=0.2,fade=t=out:st={D-0.2:.2f}:d=0.2,format=yuv420p[vout]")
    cmd = (["ffmpeg", "-v", "error", "-y", "-filter_threads", "2"] + ins + extra +
           ["-filter_complex", ";".join(fc), "-map", "[vout]", "-t", f"{D:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "20", "-maxrate", "28M", "-bufsize", "48M", "-profile:v", "high", "-level", "5.1", "-g", str(FPS * 2), out])
    subprocess.run(cmd, check=True)

def build(plat):
    W, H, picks, layout, ctitle, csub, cmedia = K.PLATFORMS[plat]
    wide = layout == "wide"; wd = f"{TMP}/{plat}"; os.makedirs(wd, exist_ok=True)
    seq = [dict(kind="cover", key="cover_" + plat, title=ctitle, sub=csub, media=cmedia)]
    seq += [dict(kind="page", key=f"p{n:02d}", pg=PG[n]) for n in picks]
    seq += [dict(kind="cover", key="end", title=K.END_TITLE, sub=K.END_SUB, media=K.END_MEDIA)]
    jobs = []
    for i, s in enumerate(seq):
        png = f"{wd}/s{i:02d}.png"
        if s["kind"] == "cover":
            vw = 1920 if wide else 1080; dpr = W / vw; vh = round(H / dpr)
            jobs.append(dict(kind="cover", png=png, vw=vw, vh=vh, dpr=dpr, html=cover_html(s["title"], s["sub"], s["media"], wide, vh)))
        elif wide:
            jobs.append(dict(kind="page", layout="wide", png=png, vw=1600, vh=900, dpr=W / 1600, html=page_html(s["pg"], "wide", 900),
                             ticker=(f"{wd}/s{i:02d}_tk.png" if s["pg"]["kind"] == "news" else None)))
        else:
            vh = round(H / (W / 1080))
            jobs.append(dict(kind="page", layout="band", png=png, vw=1080, vh=vh, dpr=W / 1080, html=page_html(s["pg"], "band", vh)))
    asyncio.run(render_layers(jobs))
    if "--layers" in sys.argv: return
    long = plat.startswith("longform"); lead = 0.5; tail = 1.2 if long else 0.6
    t = 0.0; segs = []; clips = []; srt = []
    for i, (s, j) in enumerate(zip(seq, jobs)):
        a = DUR[s["key"]]["dur"]; D = lead + a + (tail if s["kind"] == "page" else 1.0)
        out = f"{wd}/s{i:02d}.mp4"
        if not os.path.exists(out):
            if s["kind"] == "cover": seg(out, W, H, "cover", s["media"], j["png"], D)
            else: seg(out, W, H, "page", s["pg"]["media"], j["png"], D, alt=s["pg"].get("alt", False), ticker=j.get("ticker"))
        segs.append(out); clips.append((t + lead, f"{AUD}/{DUR[s['key']]['file']}"))
        srt.append((t + 0.0, t + lead + a, DUR[s["key"]]["text"])); t += D
        print(plat, i, s["key"], round(D, 2), flush=True)
    lst = f"{wd}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in segs))
    vid = f"{wd}/video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    ins = []; fl = []
    for k, (st, f) in enumerate(clips):
        ins += ["-i", f]; ms = int(st * 1000); fl.append(f"[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]")
    fl.append("".join(f"[a{k}]" for k in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{t:.3f}[aout]")
    aud = f"{wd}/narr.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[aout]", "-ac", "2", "-c:a", "aac", "-b:a", "192k", aud], check=True)
    name = f"epic_fury_ep{K.EP2}_{plat}_ko"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart",
                    "-shortest", f"{OUT}/{name}.mp4"], check=True)
    ts = lambda x: f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round((x-int(x))*1000))%1000:03d}"
    open(f"{OUT}/{name}.srt", "w").write("\n".join(f"{k+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for k, (a, b, x) in enumerate(srt)))
    print("DONE", name, round(t, 1), flush=True)

if __name__ == "__main__":
    for p in [a for a in sys.argv[1:] if not a.startswith("-")]:
        build(p)
