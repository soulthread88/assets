"""EP01 KR platform video renderer.
Per page: blurred/dimmed full-frame background + sharp 16:9 media box (Ken Burns / video) +
chrome overlay (header, panels, credit) + text overlay (fades/slides in 0.5 s before narration) +
scrolling ticker on news pages. Narration = Typecast Inhwa clips placed on a timeline."""
import os, sys, json, subprocess, html, math, asyncio
sys.path.insert(0, os.path.dirname(__file__))
import content_ko as K

ROOT = "/home/claude/work"; MEDIA = f"{ROOT}/media"; AUD = f"{ROOT}/audio"
OUT = f"{ROOT}/out"; TMP = f"{ROOT}/tmp"; os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
MAN = json.load(open(f"{MEDIA}/manifest.json")); DUR = json.load(open(f"{AUD}/durations.json"))
FPS = 30
FALLBACK = {"img_b2_depart": "img_b2_prep", "img_f15e": "img_spruance", "img_f16_fly": "img_b2_prep",
            "img_hornet": "img_ford_deck", "img_tehran_smoke": "img_borujerdi4"}
AUTHOR_FIX = {"img_b2_prep": "U.S. Air Force (DVIDS)", "img_ford_deck": "U.S. Navy (DVIDS)",
              "img_spruance": "U.S. Navy · NAVCENT Public Affairs", "img_map100h": "U.S. Department of War",
              "img_b2_depart": "U.S. Air Force (DVIDS)", "img_f15e": "U.S. Air Force (DVIDS)",
              "img_f16_fly": "U.S. Air Force (DVIDS)", "img_hornet": "U.S. Navy (DVIDS)"}
TICKER = ("미·이스라엘, 이란 전역 공습 개시 — 미 작전명 '장대한 분노', 이스라엘 작전명 '포효하는 사자'   ┃   "
          "이스라엘 \"이란 최고지도자 알리 하메네이 사망\" — 이란 정부 공식 확인은 3월 1일   ┃   "
          "이란, 보복 작전 '진실의 약속 4' 개시 — 바레인 미 5함대 시설 피격   ┃   "
          "이란 남부 미나브 여자 초등학교 피격 — 이란 매체 180명 사망 보도   ┃   "
          "이란 적신월사 \"개전 첫날 사망자 200명 이상\"   ┃   ")

def media_key(k):
    if k in MAN and os.path.exists(f"{MEDIA}/{MAN[k]['file']}"): return k
    return FALLBACK.get(k, k)

def credit(k):
    m = MAN[k]; a = AUTHOR_FIX.get(k, m.get("author") or "")
    if m["site"] == "Wikimedia Commons":
        d = (m.get("date") or "").replace("Taken on ", "")
        return f"{a} · {m['license']} · Wikimedia Commons" + (f" · {d.split(',')[0]}" if d else "")
    return f"{a} · {m['site']} (무료 라이선스) · 분위기 영상"

# ---------- geometry ----------
def geom(W, H, layout):
    if layout == "wide":
        bw, bh = 2000, 1125; ty = (H - bh) // 2 + 70
        return dict(box=(W - 140 - bw, ty, bw, bh), text=(140, ty, W - 140 - bw - 100 - 140, bh), body=66, label=40, cap=34, head=150)
    if layout == "tall":
        bw, bh = 2000, 1125
        return dict(box=(80, 640, bw, bh), text=(80, 640 + bh + 150, bw, 1350), body=82, label=48, cap=40, head=200)
    bw, bh = 2000, 1125  # feed 2160x2700
    return dict(box=(80, 330, bw, bh), text=(80, 330 + bh + 120, bw, 980), body=74, label=44, cap=38, head=170)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:transparent;width:%(W)dpx;height:%(H)dpx;overflow:hidden}
body{font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;color:#f3efe6}
.L{position:absolute}
.head{left:0;top:0;width:%(W)dpx;height:%(head)dpx;background:linear-gradient(#0b1626f2,#0b1626e0);border-bottom:4px solid #c9a227;
 display:flex;align-items:center;justify-content:space-between;padding:0 %(pad)dpx}
.head .l{font-weight:900;color:#c9a227;font-size:%(hs)dpx;letter-spacing:2px}
.head .c{text-align:center;line-height:1.15}.head .c b{display:block;font-size:%(hb)dpx;font-weight:900;color:#fff}
.head .c span{font-size:%(hs2)dpx;color:#d8cfb8;letter-spacing:6px}
.head .r{font-size:%(hs)dpx;color:#d8cfb8;font-weight:700;text-align:right}
.ep{left:0;top:%(head)dpx;width:%(W)dpx;height:%(eph)dpx;background:#0b1626d9;display:flex;align-items:center;padding:0 %(pad)dpx;border-bottom:2px solid #c9a22766}
.ep i{font-style:normal;border:3px solid #c9a227;color:#c9a227;font-weight:900;font-size:%(eps)dpx;padding:2px 14px;border-radius:6px;margin-right:24px}
.ep b{font-size:%(eps2)dpx;color:#fff;font-weight:700}
.panel{background:linear-gradient(90deg,#08111dee,#08111dcc);border-left:8px solid #c9a227;border-radius:10px}
.boxframe{border:4px solid #c9a227aa;border-radius:6px;box-shadow:0 0 60px #000c}
.cap{font-style:italic;color:#cfc6b2;font-size:%(cap)dpx;line-height:1.3;text-align:right}
.txt{display:flex;flex-direction:column;justify-content:center;padding:0 60px 0 %(mm5)dpx}
.tag{align-self:flex-start;background:#c8102e;color:#fff;font-weight:900;font-size:%(label)dpx;padding:6px 22px;border-radius:6px;margin-bottom:22px;letter-spacing:1px}
.tag.f{background:#1d3a5f;border:2px solid #c9a227;color:#f1d27a}
.lab{color:#e9c45a;font-weight:700;font-size:%(label)dpx;margin-bottom:10px}
.sub{color:#b9b0a0;font-style:italic;font-size:%(cap)dpx;margin-bottom:26px}
.body{font-family:'Noto Serif CJK KR',serif;font-weight:600;font-size:%(body)dpx;line-height:1.62;color:#fbf7ee;word-break:keep-all;text-shadow:0 2px 6px #000}
.ticker{left:0;width:%(W)dpx;height:%(tkh)dpx;background:#c8102e;display:flex;align-items:center}
.tk-l{background:#fff;color:#c8102e;font-weight:900;font-size:%(tks)dpx;padding:0 26px;height:100%%;display:flex;align-items:center;z-index:2}
/* cover */
.cv-grad{left:0;top:0;width:%(W)dpx;height:%(H)dpx;background:linear-gradient(180deg,#0b1626cc 0%%,#0b162600 14%%,#0b162600 34%%,#0b1626cc 62%%,#0b1626f5 100%%)}
.cv{left:%(cvx)dpx;bottom:%(cvb)dpx;width:%(cvw)dpx}
.chips span{display:inline-block;font-weight:900;font-size:%(chip)dpx;padding:6px 20px;border-radius:6px;margin-right:18px}
.chips .a{background:#c8102e;color:#fff}.chips .b{border:3px solid #c9a227;color:#c9a227}
.cv h1{font-weight:900;font-size:%(cvt)dpx;line-height:1.15;margin:30px 0 22px;color:#fff;text-shadow:0 6px 24px #000;word-break:keep-all}
.cv .ln{color:#e9c45a;font-weight:700;font-size:%(cvl)dpx;padding-bottom:22px;border-bottom:6px solid #c9a227;display:inline-block}
.cv .dc{margin-top:30px;color:#d8cfb8;font-size:%(cvd)dpx}
.cvtop{left:%(pad)dpx;top:%(pad)dpx;right:%(pad)dpx;display:flex;justify-content:space-between;font-weight:900;color:#c9a227;font-size:%(chip)dpx}
"""

def page_html(W, H, layout, pg, n, N, part):
    g = geom(W, H, layout); s = W / 3840 if layout == "wide" else W / 2160
    v = dict(W=W, H=H, head=g["head"], pad=int(80 if layout != "wide" else 140), hs=int(44 * (1 if layout == "wide" else 1.05)),
             hb=int(58 if layout == "wide" else 66), hs2=int(30 if layout == "wide" else 34), eph=int(90 if layout == "wide" else 104),
             eps=int(36 if layout == "wide" else 42), eps2=int(44 if layout == "wide" else 50), cap=g["cap"], label=g["label"],
             body=g["body"], mm5=38, tkh=int(96 if layout == "wide" else 110),
             tks=int(42 if layout == "wide" else 48), cvx=int(160 if layout == "wide" else 110), cvb=int(200 if layout == "wide" else 360),
             cvw=int(W - 320), chip=int(46 if layout == "wide" else 52), cvt=int(170 if layout == "wide" else 190),
             cvl=int(64 if layout == "wide" else 70), cvd=int(40 if layout == "wide" else 44))
    css = CSS % v
    e = html.escape
    kind = pg["kind"]
    if kind in ("cover", "end"):
        if part == "text":
            dc = e(K.DISCLAIMER) if kind == "cover" else "픽션 · AI 내레이션 (Typecast '인화')"
            chips = '<div class="chips"><span class="a">FICTION</span><span class="b">EP 01</span></div>'
            body = (f'<div class="L cv-grad"></div><div class="L cvtop"><span>{e(K.SERIES)} · {e(K.SUB)}</span><span>소설</span></div>'
                    f'<div class="L cv">{chips}<h1>{e(pg["title"])}</h1><div class="ln">{e(pg["line"])}</div><div class="dc">{dc}</div></div>')
        else:
            body = '<div class="L cv-grad"></div>'
        return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
    bx, by, bw, bh = g["box"]; tx, ty, tw, th = g["text"]
    if part == "chrome":
        parts = [f'<div class="L head"><div class="l">전쟁소설</div><div class="c"><b>{e(K.SERIES)}</b><span>{e(K.SUB)}</span></div>'
                 f'<div class="r">{e(K.DATE)}<br>{n}/{N}</div></div>',
                 f'<div class="L ep"><i>EP 01</i><b>{e(K.EP_TITLE)}</b></div>',
                 f'<div class="L panel" style="left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px"></div>',
                 f'<div class="L boxframe" style="left:{bx-4}px;top:{by-4}px;width:{bw+8}px;height:{bh+8}px"></div>',
                 f'<div class="L cap" style="left:{bx}px;top:{by+bh+14}px;width:{bw}px">{e(credit(media_key(pg["media"])))}</div>']
        if kind == "news":
            tky = H - v["tkh"] - (0 if layout == "wide" else 160)
            parts.append(f'<div class="L ticker" style="top:{tky}px"><div class="tk-l">소설 속보</div></div>')
        return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(parts)}</body></html>"
    # text layer
    tag = pg.get("tag") or ("FICTION · 실전 상황" if kind == "news" else None)
    tg = f'<div class="tag{" f" if tag and "FICTION" in tag or tag == "역사 메모" else ""}">{e(tag)}</div>' if tag else ""
    sub = f'<div class="sub">{e(pg["sub"])}</div>' if pg.get("sub") else ""
    t = (f'<div class="L txt" id="T" style="left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px">{tg}'
         f'<div class="lab">{e(pg["label"])}</div>{sub}<div class="body" id="B">{e(pg["text"])}</div></div>')
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{t}</body></html>"

FIT_JS = """(mx) => { const T=document.getElementById('T'), B=document.getElementById('B'); if(!T) return 0;
 let fs=mx; B.style.fontSize=fs+'px'; let n=0;
 while(T.scrollHeight>T.clientHeight+2 && fs>30 && n<200){ fs-=2; B.style.fontSize=fs+'px'; n++; } return fs; }"""

async def overlays(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for (W, H, layout, pg, n, N, base) in jobs:
            ctx = await b.new_context(viewport=dict(width=W, height=H)); pgx = await ctx.new_page()
            for part in ("chrome", "text"):
                fn = f"{base}_{part}.png"
                if os.path.exists(fn): continue
                await pgx.set_content(page_html(W, H, layout, pg, n, N, part)); await pgx.wait_for_timeout(150)
                if part == "text": await pgx.evaluate(FIT_JS, MAXF[layout])
                await pgx.screenshot(path=fn, omit_background=True)
            if pg["kind"] == "news":
                fn = f"{base}_ticker.png"
                if not os.path.exists(fn):
                    tks = 42 if layout == "wide" else 48; tkh = 96 if layout == "wide" else 110
                    await pgx.set_viewport_size(dict(width=12000, height=tkh))
                    await pgx.set_content(f"<html><body style='margin:0;background:#c8102e;height:{tkh}px;display:flex;align-items:center;"
                        f"white-space:nowrap;font:700 {tks}px Noto Sans CJK KR;color:#fff'><span id=s>{html.escape(TICKER*2)}</span></body></html>")
                    w = await pgx.evaluate("document.getElementById('s').offsetWidth")
                    await pgx.set_viewport_size(dict(width=int(w), height=tkh))
                    await pgx.screenshot(path=fn)
            await ctx.close()
        await b.close()

# ---------- segment encoder ----------
USE = {}
MAXF = {'wide': 84, 'tall': 132, 'feed': 120}
def seg(W, H, layout, pg, base, D, t_text):
    g = geom(W, H, layout); k = media_key(pg["media"]); m = MAN[k]; src = f"{MEDIA}/{m['file']}"
    bx, by, bw, bh = g["box"]
    USE[k] = USE.get(k, 0) + 1
    ins = []
    if m["type"] == "video":
        vd = float(m.get("duration") or 10)
        off = ((USE[k] - 1) * 4.3) % max(vd - 2, 1)
        ins += ["-stream_loop", "-1", "-ss", f"{off:.2f}", "-t", f"{D+0.5:.2f}", "-i", src]
    else:
        ins += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D+0.5:.2f}", "-i", src]
    out = f"{base}.mp4"
    fc = []
    full = pg["kind"] in ("cover", "end")
    zoom_dir = USE[k] % 2
    full0 = pg["kind"] in ("cover", "end")
    pre = f"fps={FPS},setpts=PTS-STARTPTS," if m["type"] == "video" else ""
    if full0:
        fc.append(f"[0:v]{pre}null[a]")
    else:
        fc.append(f"[0:v]{pre}split=2[a][b]")
    # background: cheap blur at low res
    fc.append(f"[a]scale={W//8}:{H//8}:force_original_aspect_ratio=increase,crop={W//8}:{H//8},boxblur=12:2,"
              f"scale={W}:{H}:flags=bilinear,eq=brightness={-0.05 if full else -0.22}:saturation=0.8[bg]")
    if full:
        # cover: sharp full frame with slow push-in
        Z = 1.10
        fc[-1] = (f"[a]scale={int(W*Z)}:{int(H*Z)}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H}:x='(iw-{W})/2+((iw-{W})/2)*sin(t/{D:.2f}*1.2)*{1 if zoom_dir else -1}':y='(ih-{H})/2',"
                  f"eq=brightness=-0.04[bg]")
        last = "[bg]"
    else:
        Z = 1.14
        sw, sh = int(bw * Z), int(bh * Z)
        dx = f"(iw-{bw})*({'t' if zoom_dir else f'{D:.2f}-t'})/{D:.2f}"
        fc.append(f"[b]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={bw}:{bh}:x='{dx}':y='(ih-{bh})/2'[box]")
        fc.append(f"[bg][box]overlay={bx}:{by}[v1]")
        last = "[v1]"
    idx = 1
    extra = []
    if not full:
        extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D+0.5:.2f}", "-i", f"{base}_chrome.png"]
        fc.append(f"{last}[{idx}:v]overlay=0:0[v2]"); last = "[v2]"; idx += 1
        if pg["kind"] == "news":
            tky = H - (96 if layout == "wide" else 110) - (0 if layout == "wide" else 160)
            lab = 300 if layout == "wide" else 330
            extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D+0.5:.2f}", "-i", f"{base}_ticker.png"]
            fc.append(f"[{idx}:v]format=rgba[tk]")
            fc.append(f"{last}[tk]overlay=x='{lab}-mod(t*260,w/2)':y={tky}:shortest=0[v3]"); last = "[v3]"; idx += 1
            # re-draw white label over ticker
            extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D+0.5:.2f}", "-i", f"{base}_chrome.png"]
            fc.append(f"[{idx}:v]crop={lab}:{96 if layout=='wide' else 110}:0:{tky}[lb]")
            fc.append(f"{last}[lb]overlay=0:{tky}[v4]"); last = "[v4]"; idx += 1
    # text layer: fade + slide up
    extra += ["-loop", "1", "-framerate", str(FPS), "-t", f"{D+0.5:.2f}", "-i", f"{base}_text.png"]
    fc.append(f"[{idx}:v]format=rgba,fade=t=in:st={t_text:.2f}:d=0.45:alpha=1[tx]")
    fc.append(f"{last}[tx]overlay=x=0:y='if(lt(t,{t_text:.2f}),40,max(0,40-(t-{t_text:.2f})*120))'[v5]"); last = "[v5]"
    fc.append(f"{last}fade=t=in:st=0:d=0.25,fade=t=out:st={D-0.25:.2f}:d=0.25,format=yuv420p[vout]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-filter_threads", "2"] + ins + extra + ["-filter_complex", ";".join(fc), "-map", "[vout]",
           "-t", f"{D:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
           "-maxrate", "24M" if W * H >= 3840 * 2160 else "18M", "-bufsize", "40M", "-profile:v", "high", "-level", "5.1",
           "-g", str(FPS * 2), out]
    subprocess.run(cmd, check=True)
    return out

def build(plat):
    W, H, seq, layout = K.PLATFORMS[plat]
    cov = K.COVERS[plat]
    pages = [dict(id="cover_" + plat, kind="cover", title=cov["title"], line=cov["line"], media=cov["media"], text=cov["narr"])]
    for pid in seq:
        d = dict(K.P.get(pid) or K.C[pid])
        if pid.startswith("cta_"):
            d = dict(id=pid, kind="end", title="제2화에서 계속됩니다", line=d["text"], media=d["media"], text=d["text"])
        pages.append(d)
    N = len(pages) - 1
    lead = 0.5; tail = 1.2 if plat == "longform" else (0.6 if layout == "wide" else 0.35)
    wd = f"{TMP}/{plat}"; os.makedirs(wd, exist_ok=True)
    jobs = []
    for i, pg in enumerate(pages):
        jobs.append((W, H, layout, pg, i, N, f"{wd}/p{i:02d}"))
    asyncio.run(overlays(jobs))
    t = 0.0; clips = []; segs = []; srt = []
    for i, pg in enumerate(pages):
        a = DUR[pg["id"]]["dur"]
        t_text = 0.3; t_voice = t_text + lead
        D = t_voice + a + (tail + (0.8 if pg["kind"] in ("cover", "end") else 0))
        base = f"{wd}/p{i:02d}"
        if not os.path.exists(base + ".mp4") or "--force" in sys.argv:
            seg(W, H, layout, pg, base, D, t_text)
        segs.append(base + ".mp4"); clips.append((t + t_voice, f"{AUD}/{DUR[pg['id']]['file']}"))
        srt.append((t + t_text, t + t_voice + a, pg["text"]))
        print(plat, i, pg["id"], round(D, 2), flush=True)
        t += D
    # concat video
    lst = f"{wd}/list.txt"; open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    vid = f"{wd}/video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    # narration timeline
    ins = []; fl = []
    for j, (st, f) in enumerate(clips):
        ins += ["-i", f]; ms = int(st * 1000); fl.append(f"[{j}:a]aresample=48000,adelay={ms}|{ms}[a{j}]")
    fl.append("".join(f"[a{j}]" for j in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0,"
              f"loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{t:.3f}[aout]")
    aud = f"{wd}/narr.m4a"
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl), "-map", "[aout]",
                    "-ac", "2", "-c:a", "aac", "-b:a", "192k", aud], check=True)
    name = f"epic_fury_ep01_{plat}_ko"
    final = f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c", "copy",
                    "-movflags", "+faststart", "-shortest", final], check=True)
    def ts(x):
        h = int(x // 3600); m_ = int(x % 3600 // 60); s_ = x % 60
        return f"{h:02d}:{m_:02d}:{int(s_):02d},{int(round((s_ - int(s_)) * 1000)):03d}"
    open(f"{OUT}/{name}.srt", "w").write("\n".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{x}\n" for i, (a, b, x) in enumerate(srt)))
    json.dump(dict(platform=plat, W=W, H=H, duration=round(t, 2), pages=[p["id"] for p in pages]),
              open(f"{OUT}/{name}.json", "w"), ensure_ascii=False)
    print("DONE", final, round(t, 1))

if __name__ == "__main__":
    for p in [a for a in sys.argv[1:] if not a.startswith("--")]:
        build(p)
