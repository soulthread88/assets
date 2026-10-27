"""EP01 KR platform videos — same structure/frames as the old mp4 set (longform template v2).
wide (16:9): template v2 desktop stage (1600x900 CSS, scaled). band (9:16 / 4:5): full-width stage band
(header / headline / media+text / breaking) over a blurred copy of the same media. Cover + pages + end card."""
import os, sys, json, subprocess, html, asyncio
sys.path.insert(0, os.path.dirname(__file__))
import content_v2 as K
ROOT = "/home/claude/work"; MEDIA = f"{ROOT}/media"; AUD = f"{ROOT}/audio2"; OUT = f"{ROOT}/out2"; TMP = f"{ROOT}/tmp2"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
MAN = json.load(open(f"{MEDIA}/manifest.json")); DUR = json.load(open(f"{AUD}/durations.json"))
FPS = 30; E = html.escape
PG = {p["n"]: p for p in K.PAGES}

FONTS = """
@font-face{font-family:'NSK';src:local('Noto Sans CJK KR');}
:root{--navy:#06152d;--gold:#f4bd3f;--white:#f7f8fa;--red:#d92d3a;
--ui:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--tts:"Noto Sans KR","Noto Sans CJK KR",sans-serif;--serif:"Noto Serif KR","Noto Serif CJK KR",serif}
*{box-sizing:border-box;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
html,body{margin:0;padding:0;background:transparent;color:var(--white);font-family:var(--ui);overflow:hidden}
"""
# ---------------- template v2 (desktop) — copied rules, media transparent ----------------
WIDE_CSS = FONTS + """
.stage{position:relative;width:1600px;height:900px;overflow:hidden;background:transparent}
.header{height:14%;display:grid;grid-template-columns:32% 36% 32%;grid-template-areas:"bl logo dt";align-items:end;padding:0 2.2% 1.5mm;margin-top:2mm;background:linear-gradient(180deg,#06152d,#07182f);border-bottom:1px solid var(--gold);position:relative;z-index:20;overflow:hidden}
.brand-left{grid-area:bl;text-align:left;font-size:22px;line-height:1.2;font-weight:800;color:var(--gold);letter-spacing:.02em}
.logo{grid-area:logo;display:flex;flex-direction:column;align-items:center}
.logo .l1{text-align:center;font-weight:800;font-size:30px;margin:0;text-shadow:2px 2px 4px #000}
.logo .l2{text-align:center;font-weight:700;font-size:20px;color:var(--gold);margin:0;margin-top:1mm}
.datetime{grid-area:dt;display:flex;align-items:baseline;justify-content:flex-end;gap:18px;text-align:right;line-height:1}
.datetime .date{font-size:20px;font-weight:700;color:var(--gold)}
.datetime .part{font-size:16px;font-weight:600;color:#fff;opacity:.85}
.header--slim .datetime .date{display:none}
.headline{height:9%;display:flex;align-items:flex-end;justify-content:center;gap:1.6%;padding:0 2.2% 1.5mm;margin-top:1.5mm;background:#071a34;border-bottom:1px solid var(--gold);overflow:hidden}
.section{flex:0 0 auto;border:2px solid var(--gold);color:var(--gold);padding:.35% 1.1%;font-size:17px;font-weight:800;white-space:nowrap}
.headline h1{margin:0;flex:1 1 auto;min-width:0;font-size:30px;font-weight:500;line-height:1.18;padding-bottom:.12em;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:2px 2px 5px #000}
.video{position:absolute;left:0;right:0;top:calc(23% + 2mm);bottom:16.2%;overflow:hidden;background:transparent}
.video:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(2,9,20,.58) 0%,rgba(2,9,20,.40) 50%,rgba(2,9,20,.12) 85%),linear-gradient(180deg,rgba(0,0,0,0) 42%,rgba(0,0,0,.12) 62%,rgba(0,0,0,.5) 100%)}
.chyron{position:absolute;left:3.1%;top:53.4%;transform:translateY(-50%);width:86%;z-index:5}
.meta{margin-bottom:1%;display:flex;flex-direction:column;align-items:flex-start;gap:7px}
.meta-tag{display:inline-block;border:2px solid var(--red);color:#fff;background:rgba(217,45,58,.75);font-weight:800;letter-spacing:.04em;padding:.25em .8em;font-size:19px;white-space:nowrap}
.meta-loc{color:var(--gold);font-size:17px;font-weight:600;letter-spacing:.035em;text-shadow:2px 2px 3px #000}
.caption{font-family:var(--tts);font-size:48px;font-weight:400;line-height:1.28;letter-spacing:-.008em;color:#fff;text-shadow:2px 3px 4px #000;text-align:justify;text-justify:inter-character;word-break:normal;overflow-wrap:break-word}
.breaking{position:absolute;left:0;right:0;bottom:calc(3mm + 5%);display:flex;align-items:center;gap:16px;padding:1mm 2.2%;background:var(--red);z-index:10;white-space:nowrap;overflow:hidden}
.breaking .tag{flex:0 0 auto;background:#fff;color:var(--red);font-weight:700;letter-spacing:.05em;padding:.22em .9em;border-radius:4px;font-size:22px}
.breaking .items{color:#fff;font-weight:600;font-size:22px;overflow:hidden;text-overflow:ellipsis;text-shadow:1px 1px 2px rgba(0,0,0,.4)}
.breaking .dot{margin:0 .8em;color:#fff;opacity:.85}
.ticker{position:absolute;left:0;right:0;bottom:3mm;height:5%;display:flex;align-items:center;padding:0 7mm 0 2.2%;background:#06152d;border-top:1px solid var(--gold);z-index:11;overflow:hidden;font-size:19px}
.ticker .title{flex:0 0 auto;display:flex;align-items:center;line-height:1;color:var(--gold);font-weight:800;letter-spacing:.02em;border:1px solid var(--gold);border-radius:2px;background:rgba(244,189,63,.08);padding:.5mm .9em;margin-right:1.1%;white-space:nowrap}
.ticker-window{flex:1 1 auto;position:relative;height:100%;overflow:hidden}
.novel-media{position:absolute;left:0;right:0;top:calc(14% + 2mm);bottom:0;overflow:hidden;background:transparent}
.novel-media:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(2,9,20,.84) 0%,rgba(2,9,20,.66) 45%,rgba(2,9,20,.22) 78%,rgba(2,9,20,0) 100%),linear-gradient(180deg,rgba(2,9,20,0) 40%,rgba(2,9,20,.6) 100%)}
.novel-content{position:absolute;top:calc(14% + 2mm);bottom:0;left:0;right:0;z-index:4;display:flex;flex-direction:column;align-items:flex-start;justify-content:center;gap:16px;padding:0 26.9% 0 3.1%}
.novel-heading{display:flex;align-items:baseline;flex-wrap:wrap;gap:8px}
.novel-heading .scene-tag{color:var(--gold);font-weight:700;font-size:18px;letter-spacing:.03em;text-shadow:1px 1px 3px #000}
.novel-heading h2{margin:0;font-size:18px;font-weight:500;font-style:italic;color:rgba(255,255,255,.78);text-shadow:1px 1px 3px #000}
.novel-heading h2::before{content:'— '}
.novel-text{width:100%}
.novel-text p{margin:0 0 14px;font-family:var(--serif);font-size:38px;line-height:1.55;font-weight:400;color:#fff;text-shadow:1px 2px 6px rgba(0,0,0,.8);text-align:justify;text-justify:inter-character;word-break:normal;overflow-wrap:break-word}
.novel-text p:last-child{margin-bottom:0}
.novel-end{color:var(--gold)!important;font-weight:800!important;text-align:left!important}
"""
# ---------------- band (9:16, 4:5) — measured from the old 1080-wide frames ----------------
BAND_CSS = FONTS + """
.stage{position:absolute;left:0;width:1080px;background:transparent}
.header{height:99px;display:grid;grid-template-columns:32% 36% 32%;align-items:end;padding:0 34px 10px;background:linear-gradient(180deg,#06152d,#07182f);border-bottom:2px solid var(--gold)}
.brand-left{text-align:left;font-size:26px;line-height:1.2;font-weight:800;color:var(--gold);letter-spacing:.02em}
.logo{display:flex;flex-direction:column;align-items:center}
.logo .l1{font-weight:800;font-size:32px;line-height:1.2;text-shadow:2px 2px 4px #000}
.logo .l2{font-weight:700;font-size:19px;color:var(--gold);margin-top:4px}
.datetime{display:flex;align-items:baseline;justify-content:flex-end;gap:18px;line-height:1}
.datetime .date{font-size:21px;font-weight:700;color:var(--gold)}
.datetime .part{font-size:19px;font-weight:600;color:#fff;opacity:.85}
.header--slim .datetime .date{display:none}
.headline{height:65px;display:flex;align-items:center;padding:0 34px;background:#071a34;border-bottom:2px solid var(--gold);position:relative}
.section{position:absolute;left:34px;border:2px solid var(--gold);color:var(--gold);padding:3px 12px;font-size:19px;font-weight:800;white-space:nowrap}
.headline h1{margin:0;width:100%;font-size:28px;font-weight:500;text-align:center;white-space:nowrap;text-shadow:2px 2px 5px #000}
.row{position:relative;padding:50px 34px 54px}
.row:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,9,20,.58) 0%,rgba(2,9,20,.78) 100%);z-index:0}
.row>*{position:relative;z-index:1}
.meta{display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin-bottom:12px}
.meta-tag{display:inline-block;border:2px solid var(--red);color:#fff;background:rgba(217,45,58,.85);font-weight:800;letter-spacing:.04em;padding:5px 14px;font-size:22px;white-space:nowrap}
.meta-loc{color:var(--gold);font-size:20px;font-weight:600;letter-spacing:.035em;text-shadow:2px 2px 3px #000}
.caption{font-family:var(--tts);font-size:50px;font-weight:400;line-height:1.3;color:#fff;text-shadow:2px 3px 4px #000;text-align:justify;text-justify:inter-character;word-break:normal;overflow-wrap:break-word}
.breaking{height:56px;display:flex;align-items:center;gap:14px;padding:0 34px;background:var(--red);white-space:nowrap;overflow:hidden}
.breaking .tag{flex:0 0 auto;background:#fff;color:var(--red);font-weight:700;letter-spacing:.05em;padding:3px 12px;border-radius:4px;font-size:21px}
.breaking .items{color:#fff;font-weight:600;font-size:20px;overflow:hidden;text-overflow:ellipsis}
.breaking .dot{margin:0 .6em}
.novel-heading{display:flex;align-items:baseline;flex-wrap:wrap;gap:10px;margin-bottom:22px}
.novel-heading .scene-tag{color:var(--gold);font-weight:700;font-size:21px;letter-spacing:.03em;text-shadow:1px 1px 3px #000}
.novel-heading h2{margin:0;font-size:21px;font-weight:500;font-style:italic;color:rgba(255,255,255,.78)}
.novel-heading h2::before{content:'— '}
.novel-text p{margin:0 0 14px;font-family:var(--serif);font-size:48px;line-height:1.5;font-weight:400;color:#fff;text-shadow:1px 2px 6px rgba(0,0,0,.8);text-align:justify;text-justify:inter-character;word-break:normal;overflow-wrap:break-word}
.novel-text p:last-child{margin-bottom:0}
.novel-end{color:var(--gold)!important;font-weight:800!important;text-align:left!important;font-size:38px!important}
"""
# ---------------- cover / end card (measured from old covers) ----------------
def cover_css(wide):
    b = 1920 if wide else 1080
    s = dict(pad=84 if wide else 34, top=82 if wide else 58, tf=30 if wide else 28, pill=36 if wide else 28,
             t=134 if wide else 112, sub=50 if wide else 40, barw=492 if wide else 376, barh=8 if wide else 6,
             blk="44%" if wide else "52.7%")
    return FONTS + f"""
.cv{{position:absolute;left:0;top:0;width:{b}px;height:var(--H);background:linear-gradient(180deg,rgba(2,9,20,.45) 0%,rgba(2,9,20,.30) 35%,rgba(2,9,20,.62) 70%,rgba(2,9,20,.82) 100%)}}
.top{{position:absolute;left:{s['pad']}px;right:{s['pad']}px;top:{s['top']}px;display:flex;justify-content:space-between;color:var(--gold);font-weight:800;font-size:{s['tf']}px;text-shadow:0 2px 6px #000}}
.blk{{position:absolute;left:{s['pad']}px;right:{s['pad']}px;top:{s['blk']}}}
.pills span{{display:inline-block;font-weight:800;font-size:{s['pill']}px;padding:.18em .55em;margin-right:.6em;letter-spacing:.05em;vertical-align:top}}
.pills .a{{background:#e0383e;color:#fff;border:2px solid #e0383e}}.pills .b{{border:2px solid var(--gold);color:var(--gold)}}
h1{{margin:.42em 0 0;font-weight:900;font-size:{s['t']}px;line-height:1.12;color:#fff;letter-spacing:-.01em;text-shadow:0 4px 14px rgba(0,0,0,.7);word-break:keep-all}}
.sub{{margin-top:.55em;color:var(--gold);font-weight:700;font-size:{s['sub']}px}}
.bar{{margin-top:{int(s['sub']*1.3)}px;width:{s['barw']}px;height:{s['barh']}px;background:var(--gold)}}
"""

def header(n, slim):
    return (f'<header class="header{" header--slim" if slim else ""}"><div class="brand-left">전쟁소설</div>'
            f'<div class="logo"><span class="l1">장대한 분노</span><span class="l2">호르무즈의 밤</span></div>'
            f'<div class="datetime"><span class="date">{K.DATE}</span><span class="part">{n}/21</span></div></header>')

def page_html(pg, layout, H):
    n = pg["n"]; news = pg["kind"] == "news"
    brk = (f'<section class="breaking"><span class="tag">소설 속보</span><span class="items">{E(K.BREAKING[0])}'
           f'<span class="dot">|</span>{E(K.BREAKING[1])}</span></section>')
    hl = f'<section class="headline"><div class="section">EP {K.EP2}</div><h1>제 {K.EP_NO}화 - {E(K.SUBTITLE)}</h1></section>'
    if news:
        txt = (f'<div class="meta"><span class="meta-tag">FICTION · 실전 상황</span><span class="meta-loc">{E(pg["loc"])}</span></div>'
               f'<div class="caption" id="T">{E(pg["text"])}</div>')
    else:
        h2 = f'<h2>{E(pg["h2"])}</h2>' if pg.get("h2") else ""
        end = f'<p class="novel-end">{E(K.END_NOTE)}</p>' if pg.get("end") else ""
        txt = (f'<div class="novel-heading"><span class="scene-tag">{E(pg["tag"])}</span>{h2}</div>'
               f'<div class="novel-text" id="T"><p>{E(pg["text"])}</p>{end}</div>')
    if layout == "wide":
        if news:
            tk = "".join(f'{E(x)}<span class="dot">|</span>' for x in K.TICKER)
            body = (header(n, False) + hl + '<section class="video" id="M"></section>' + f'<section class="chyron">{txt}</section>' + brk +
                    f'<footer class="ticker"><span class="title">주요사건 타임라인</span><div class="ticker-window" id="TW"></div></footer>')
        else:
            body = header(n, True) + '<section class="novel-media" id="M"></section>' + f'<div class="novel-content">{txt}</div>'
        return f"<!doctype html><html><head><meta charset='utf-8'><style>{WIDE_CSS}</style></head><body><main class='stage'>{body}</main></body></html>"
    body = header(n, not news) + (hl if news else "") + f'<section class="row" id="M">{txt}</section>' + (brk if news else "")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{BAND_CSS}</style></head><body style='width:1080px;height:{H}px'>"
            f"<main class='stage' id='S'>{body}</main></body></html>")

def cover_html(title, sub, wide, H):
    b = 1920 if wide else 1080
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{cover_css(wide)}</style></head>"
            f"<body style='width:{b}px;height:{H}px;--H:{H}px'><div class='cv'></div>"
            f"<div class='top'><span>장대한 분노 · 호르무즈의 밤</span><span>소설</span></div>"
            f"<div class='blk'><div class='pills'><span class='a'>FICTION</span><span class='b'>EP {K.EP2}</span></div>"
            f"<h1>{E(title)}</h1><div class='sub'>{E(sub)}</div><div class='bar'></div></div></body></html>")

async def render_layers(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for j in jobs:
            if os.path.exists(j["png"]): continue
            ctx = await br.new_context(viewport=dict(width=j["vw"], height=j["vh"]), device_scale_factor=j["dpr"])
            pg = await ctx.new_page(); await pg.set_content(j["html"]); await pg.wait_for_timeout(200)
            info = {}
            if j["kind"] == "page":
                if j["layout"] == "band":
                    # fit text (shrink if needed), then centre the band vertically
                    await pg.evaluate("""(H)=>{const S=document.getElementById('S');let h=S.offsetHeight;
                        const T=document.getElementById('T'); let el=T.querySelector('p')||T; let fs=parseFloat(getComputedStyle(el).fontSize);
                        while(S.offsetHeight>H*0.78 && fs>30){fs-=1; el.style.fontSize=fs+'px';}
                        h=S.offsetHeight; S.style.top=Math.round(H*%f-h/2)+'px';}""" % j["center"], j["vh"])
                else:
                    await pg.evaluate("""()=>{const T=document.getElementById('T');const box=T.closest('.chyron,.novel-content');
                        let el=T.querySelector('p')||T; let fs=parseFloat(getComputedStyle(el).fontSize);
                        const lim = box.classList.contains('chyron') ? document.getElementById('M').getBoundingClientRect() : box.getBoundingClientRect();
                        const over=()=>{const r=box.classList.contains('chyron')?box.getBoundingClientRect():T.getBoundingClientRect(); return r.top<lim.top+8||r.bottom>lim.bottom-8;};
                        while(over() && fs>24){fs-=1; el.style.fontSize=fs+'px';}}""")
                info = await pg.evaluate("""()=>{const r=e=>{if(!e)return null;const b=e.getBoundingClientRect();return [b.left,b.top,b.width,b.height]};
                    return {M:r(document.getElementById('M')),TW:r(document.getElementById('TW')),S:r(document.getElementById('S'))}}""")
            await pg.screenshot(path=j["png"], omit_background=True)
            json.dump({k: ([round(x * j["dpr"]) for x in v] if v else None) for k, v in info.items()}, open(j["png"] + ".json", "w"))
            if j.get("ticker"):
                tk = "".join(f'{E(x)}<span style="margin:0 .7em">|</span>' for x in K.TICKER) * 2
                th = round(info["TW"][3])
                await pg.set_viewport_size(dict(width=8000, height=th))
                await pg.set_content(f"<!doctype html><html><head><style>{FONTS}</style></head><body style='margin:0;height:{th}px;background:#06152d;"
                                     f"display:flex;align-items:center;white-space:nowrap;font:400 19px var(--ui);color:#fff'><span id=s>{tk}</span></body></html>")
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

def seg(out, W, H, layout, kind, key, png, D, alt=False, ticker=None, news=False):
    ins, isvid = media_input(key, D, alt)
    geo = json.load(open(png + ".json"))
    pre = f"fps={FPS},setpts=PTS-STARTPTS," if isvid else ""
    fc = []; idx = 1; extra = ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", png]
    zoom = f"1.08+0.04*t/{D:.2f}" if alt else f"1.0+0.05*t/{D:.2f}"
    def fit(w, h, lab, src, z):
        # cover-scale with slow push-in (zoom expressed via crop of an oversized frame)
        Z = 1.14 if z else 1.0
        return (f"{src}scale={int(w*Z)}:{int(h*Z)}:force_original_aspect_ratio=increase,"
                f"crop={w}:{h}:x='(iw-{w})/2+(iw-{w})/2*sin(t/{D:.2f}*1.4)*0.6':y='(ih-{h})/2'{lab}")
    if kind == "cover":
        fc.append(fit(W, H, ",eq=brightness=-0.06:saturation=0.9[v0]", f"[0:v]{pre}", True)); last = "[v0]"
    else:
        x, y, w, h = geo["M"]
        if layout == "band":
            fc.append(f"[0:v]{pre}split=2[a][b]")
            fc.append(f"[a]scale={W//8}:{H//8}:force_original_aspect_ratio=increase,crop={W//8}:{H//8},boxblur=10:2,scale={W}:{H}:flags=bilinear,eq=brightness=-0.06:saturation=0.9:gamma=1.15[bg]")
            fc.append(fit(w, h, ",eq=contrast=1.06:saturation=0.95[box]", "[b]", True))
            fc.append(f"[bg][box]overlay={x}:{y}[v0]")
        else:
            fc.append(f"color=c=0x06152d:s={W}x{H}:r={FPS}:d={D+.5:.2f}[bg]")
            filt = ",eq=contrast=1.08:saturation=0.98[box]" if news else ",eq=contrast=1.05:saturation=0.92:brightness=-0.06[box]"
            fc.append(fit(w, h, filt, f"[0:v]{pre}", True))
            fc.append(f"[bg][box]overlay={x}:{y}:shortest=1[v0]")
        last = "[v0]"
    fc.append(f"[{idx}:v]format=rgba[ov]"); fc.append(f"{last}[ov]overlay=0:0[v1]"); last = "[v1]"; idx += 1
    if ticker:
        tx, ty, tw, th = geo["TW"]
        extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D + .5:.2f}", "-i", ticker]
        sw = int(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=width", "-of", "csv=p=0", ticker]))
        fc.append(f"[{idx}:v]scale=-1:{th},crop={tw}:{th}:x='mod(t*{int(W/3840*190)}+{(USE.get('_tk',0)*997)%sw},iw/2)':y=0[tk]")
        USE["_tk"] = USE.get("_tk", 0) + 1
        fc.append(f"{last}[tk]overlay={tx}:{ty}[v2]"); last = "[v2]"; idx += 1
    fc.append(f"{last}fade=t=in:st=0:d=0.2,fade=t=out:st={D-0.2:.2f}:d=0.2,format=yuv420p[vout]")
    cmd = (["ffmpeg", "-v", "error", "-y", "-filter_threads", "2"] + ins + extra +
           ["-filter_complex", ";".join(fc), "-map", "[vout]", "-t", f"{D:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "21", "-maxrate", "24M", "-bufsize", "40M", "-profile:v", "high", "-level", "5.1", "-g", str(FPS * 2), out])
    subprocess.run(cmd, check=True)

def build(plat):
    W, H, picks, layout, ctitle, csub, cmedia = K.PLATFORMS[plat]
    wide = layout == "wide"
    wd = f"{TMP}/{plat}"; os.makedirs(wd, exist_ok=True)
    seq = [dict(kind="cover", key="cover_" + plat, title=ctitle, sub=csub, media=cmedia)]
    seq += [dict(kind="page", key=f"p{n:02d}", pg=PG[n]) for n in picks]
    seq += [dict(kind="cover", key="end", title=K.END_TITLE, sub=K.END_SUB, media=K.END_MEDIA)]
    jobs = []
    for i, s in enumerate(seq):
        png = f"{wd}/s{i:02d}.png"
        if s["kind"] == "cover":
            vw = 1920 if wide else 1080; dpr = W / vw
            jobs.append(dict(kind="cover", png=png, vw=vw, vh=round(H / dpr), dpr=dpr, html=cover_html(s["title"], s["sub"], wide, round(H / dpr))))
        else:
            if wide:
                jobs.append(dict(kind="page", layout="wide", png=png, vw=1600, vh=900, dpr=W / 1600, html=page_html(s["pg"], "wide", 900),
                                 ticker=(f"{wd}/s{i:02d}_tk.png" if s["pg"]["kind"] == "news" else None)))
            else:
                vh = round(H / (W / 1080))
                jobs.append(dict(kind="page", layout="band", png=png, vw=1080, vh=vh, dpr=W / 1080, html=page_html(s["pg"], "band", vh),
                                 center=0.41 if H > W * 1.5 else 0.45))
    asyncio.run(render_layers(jobs))
    long = plat == "longform"; lead = 0.5; tail = 1.2 if long else 0.6
    t = 0.0; segs = []; clips = []; srt = []
    for i, (s, j) in enumerate(zip(seq, jobs)):
        a = DUR[s["key"]]["dur"]; D = lead + a + (tail if s["kind"] == "page" else 1.0)
        out = f"{wd}/s{i:02d}.mp4"
        if not os.path.exists(out):
            if s["kind"] == "cover":
                seg(out, W, H, layout, "cover", s["media"], j["png"], D)
            else:
                pg = s["pg"]
                seg(out, W, H, layout, "page", pg["media"], j["png"], D, alt=pg.get("alt", False), ticker=j.get("ticker"), news=pg["kind"] == "news")
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
    name = f"epic_fury_ep01_{plat}_ko"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart",
                    "-shortest", f"{OUT}/{name}.mp4"], check=True)
    ts = lambda x: f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round((x-int(x))*1000))%1000:03d}"
    open(f"{OUT}/{name}.srt", "w").write("\n".join(f"{k+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for k, (a, b, x) in enumerate(srt)))
    print("DONE", name, round(t, 1), flush=True)

if __name__ == "__main__":
    for p in [a for a in sys.argv[1:] if not a.startswith("-")]:
        if "--layers" in sys.argv:
            pass
        build(p)
