# -*- coding: utf-8 -*-
"""Per-platform dynamic "video html" for EP01 (ko/en/jp): the same slides as the platform MP4
(cover → pages → end card), built from the exact overlay layers the renderer uses, with live media,
narration, auto-advance, Kor|Eng|Jpn + Dark/Light menu, and click-to-show replace/delete media tools.
All images, clips and narration load from GitHub (soulthread88) every time the page opens.
Usage: python3 make_platform_html.py LANG PLAT OUTDIR"""
import os, sys, json, html, importlib
sys.path.insert(0, os.path.dirname(__file__))
LANG, PLAT, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
R = importlib.import_module({"ko": "render_v2", "en": "render_en", "jp": "render_jp"}[LANG])
K = R.K; E = html.escape
RAW = "https://raw.githubusercontent.com/soulthread88"
MAN = json.load(open("/home/claude/work/media/manifest.json"))
AUTHOR_FIX = {"img_b2_prep": "U.S. Air Force (DVIDS)", "img_ford_deck": "U.S. Navy (DVIDS)",
              "img_spruance": "U.S. Navy · NAVCENT Public Affairs", "img_map100h": "U.S. Department of War"}
AUD = f"{RAW}/audio/main/novel/ep01/{LANG}_v2"
UI = getattr(K, "UI", None) or dict(html_lang="ko", rep="교체", dele="삭제", aria="내레이션 재생", light="☀ Light", dark="🌙 Dark",
                                     l1="장대한 분노", l2="호르무즈의 밤")
FONT_LINK = {
 "ko": "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&family=Noto+Serif+KR:wght@400;500;700&display=swap",
 "en": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Playfair+Display:wght@700;800;900&display=swap",
 "jp": "https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800;900&family=Noto+Serif+JP:wght@400;500;700&family=Shippori+Mincho:wght@600;700;800&display=swap",
}[LANG]
PLAT_NAME = {"ko": dict(longform="롱폼", x="X", facebook="페이스북", shorts="유튜브 쇼츠", reels="인스타그램 릴스", tiktok="틱톡", threads="스레드", feeds="인스타그램 피드"),
             "en": dict(longform="Longform", x="X", facebook="Facebook", shorts="YouTube Shorts", reels="Instagram Reels", tiktok="TikTok", threads="Threads", feeds="Instagram Feed"),
             "jp": dict(longform="ロングフォーム", x="X", facebook="Facebook", shorts="YouTube ショート", reels="Instagram リール", tiktok="TikTok", threads="Threads", feeds="Instagram フィード")}[LANG]
T = {"ko": dict(title=f"장대한 분노 · 호르무즈의 밤 — 제1화 {K.SUBTITLE}", mp4="MP4 영상", fiction="픽션 · AI 내레이션", sec="초",
                desc="미국·이스라엘의 대이란 작전에서 착상한 전쟁 소설 1화를 플랫폼 영상과 같은 화면 순서로 보여 줍니다. 등장인물과 대화는 창작입니다."),
     "en": dict(title=f"Epic Fury: Night Over Hormuz — Episode 1: {K.SUBTITLE}", mp4="MP4 video", fiction="Fiction · AI narration", sec="s",
                desc="Episode 1 of a war novel inspired by the U.S.–Israeli strikes on Iran, shown in the same screen order as the platform video. Characters and dialogue are fictional."),
     "jp": dict(title=f"エピック・フューリー：ホルムズの夜 ― 第1話 {K.SUBTITLE}", mp4="MP4動画", fiction="フィクション · AIナレーション", sec="秒",
                desc="米・イスラエルの対イラン作戦に着想を得た戦争小説の第1話を、プラットフォーム動画と同じ画面の順番で見せます。登場人物と会話は創作です。")}[LANG]

W, H, picks, layout, ctitle, csub, cmedia = K.PLATFORMS[PLAT]
wide = layout == "wide"

def murl(k):
    m = MAN[k]
    if m["type"] == "video": return f"{RAW}/videos/main/novel/ep01/platform_ko/source/{m['file']}"
    return f"{RAW}/imgs/main/novel/ep01/platform_ko/{m['file']}"

def credit(k):
    m = MAN[k]; a = AUTHOR_FIX.get(k, m.get("author") or "")
    return f'{E(a)} · {E(m.get("license") or "")} · <a href="{E(m["page"])}" target="_blank" rel="noopener">{E(m["site"])}</a>'

def media_tag(k, alt=False):
    m = MAN[k]; u = murl(k)
    st = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1"
    if m["type"] == "video":
        return f'<video data-media autoplay muted loop playsinline preload="metadata" style="{st}" src="{u}{"#t=3" if alt else ""}"></video>'
    return f'<img data-media alt="" style="{st}" src="{u}">'

TICKER_CSS = ("<style>#TW .tk{position:absolute;left:0;top:0;height:100%;display:flex;align-items:center;white-space:nowrap;"
              "font:400 19px var(--ui);color:#fff;animation:tk 60s linear infinite}#TW .tk i{font-style:normal;margin:0 .7em}"
              "@keyframes tk{from{transform:translateX(0)}to{transform:translateX(-50%)}}</style>")

def overlay(kind, pg=None, title=None, sub=None, mk=None, vh=None):
    """Return (srcdoc, native_w, native_h) — the renderer's overlay document with live media injected."""
    link = f"<link rel='stylesheet' href='{FONT_LINK}'>"
    if kind == "cover":
        vw = 1920 if wide else 1080; vh = round(H / (W / vw))
        doc = R.cover_html(title, sub, wide, vh)
        doc = doc.replace("<body ", "<body class='cover' ", 1)
        doc = doc.replace("<div class='cv'></div>", f"<div style='position:absolute;inset:0;overflow:hidden;filter:brightness(.94) saturate(.9)'>{media_tag(mk)}</div><div class='cv'></div>", 1)
    else:
        if wide:
            vw, vh = 1600, 900
            doc = R.page_html(pg, "wide", 900)
            doc = doc.replace('id="M"></section>', f'id="M">{media_tag(pg["media"], pg.get("alt"))}</section>', 1)
            doc = doc.replace("<body>", "<body style='background:#06152d'>", 1)
            if 'id="TW"' in doc:
                tk = "".join(f"{E(x)}<i>|</i>" for x in K.TICKER) * 2
                doc = doc.replace('<div class="ticker-window" id="TW"></div>', f'<div class="ticker-window" id="TW"><span class="tk">{tk}</span></div>', 1)
                doc = doc.replace("</head>", TICKER_CSS + "</head>", 1)
        else:
            vw = 1080; vh = round(H / (W / 1080))
            doc = R.page_html(pg, "band", vh)
            doc = doc.replace('<section class="row" id="M">', f'<section class="row" id="M">{media_tag(pg["media"], pg.get("alt"))}', 1)
            # centre the band like the renderer (0.41H for 9:16, 0.45H for 4:5) and shrink text if it overflows
            c = 0.41 if H > W * 1.5 else 0.45
            doc = doc.replace("</body>", f"<script>addEventListener('load',function(){{var S=document.getElementById('S'),H={vh};"
                              "var T=document.getElementById('T'),el=T.querySelector('p')||T,fs=parseFloat(getComputedStyle(el).fontSize);"
                              f"while(S.offsetHeight>H*0.78&&fs>30){{fs-=1;el.style.fontSize=fs+'px';}}S.style.top=Math.round(H*{c}-S.offsetHeight/2)+'px';}});"
                              "document.fonts&&document.fonts.ready.then(function(){dispatchEvent(new Event('load'))});</script></body>", 1)
    doc = doc.replace("<meta charset='utf-8'>", "<meta charset='utf-8'>" + link, 1)
    return doc, vw, vh

slides = [dict(kind="cover", key="cover_" + PLAT, title=ctitle, sub=csub, media=cmedia)]
slides += [dict(kind="page", key=f"p{n:02d}", pg=R.PG[n], media=R.PG[n]["media"]) for n in picks]
slides += [dict(kind="cover", key="end", title=K.END_TITLE, sub=K.END_SUB, media=K.END_MEDIA)]

ratio = f"{W} / {H}"
parts = []
for i, s in enumerate(slides):
    if s["kind"] == "cover":
        doc, vw, vh = overlay("cover", title=s["title"], sub=s["sub"], mk=s["media"])
        alt = False
    else:
        doc, vw, vh = overlay("page", pg=s["pg"])
        alt = s["pg"].get("alt", False)
    bg = ""
    if not wide and s["kind"] == "page":
        bg = f'<div class="blur">{media_tag(s["media"], alt).replace("z-index:-1", "z-index:0")}</div>'
    parts.append(
        f'\n<main class="stage slide" data-i="{i}">\n'
        f'<audio class="narration" id="narr-{i}" preload="none"><source src="{AUD}/ep01_{LANG}_{s["key"]}.mp3" type="audio/mpeg"></audio>\n'
        f'<div class="fit mbox" data-mkey="{PLAT}_{i:02d}" data-w="{vw}" data-h="{vh}">{bg}'
        f'<iframe class="ov" title="slide {i+1}" scrolling="no" width="{vw}" height="{vh}" srcdoc="{E(doc, quote=True)}"></iframe>'
        f'<div class="imgtools" hidden><button type="button" class="btn-rep">{E(UI["rep"])}</button><button type="button" class="btn-del">{E(UI["dele"])}</button>'
        f'<input type="file" accept="image/*,video/*" hidden></div>'
        f'<button class="narr-btn" type="button" data-target="narr-{i}" aria-label="{E(UI["aria"])}"><span class="narr-icon">▶</span></button></div>\n'
        f'<p class="credit">{credit(s["media"])}</p>\n</main>')

def nav():
    items = [("ko", "Kor", "ko"), ("en", "Eng", "en"), ("jp", "Jpn", "ja")]
    return '<span class="lang">' + ' <span>|</span> '.join(
        f'<a href="epic_fury_ep01_{PLAT}_{c}.html"{" aria-current=\"page\"" if c == LANG else ""} lang="{hl}">{lab}</a>' for c, lab, hl in items) + '</span>'

mp4 = f"epic_fury_ep01_{PLAT}_{LANG}.mp4"
loc = "/home/claude/work/" + {"ko": "out2", "en": "out_en", "jp": "out_jp"}[LANG] + "/" + mp4
big = os.path.exists(loc) and os.path.getsize(loc) > 95e6
MP4URL = (f"https://media.githubusercontent.com/media/soulthread88/videos/main/novel/ep01/platform_{LANG}/{mp4}" if big
          else f"{RAW}/videos/main/novel/ep01/platform_{LANG}/{mp4}")
maxw = "1280px" if wide else ("520px" if H > W * 1.5 else "640px")

CSS = f"""
:root{{--navy:#06152d;--gold:#f4bd3f;--bg:#020914;--fg:#f7f8fa;--muted:rgba(247,248,250,.72)}}
:root[data-theme="light"]{{--bg:#e9edf3;--fg:#06152d;--muted:#3b4a63}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,sans-serif}}
.site-bar{{position:sticky;top:0;z-index:100;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 5mm;background:rgba(2,9,20,.92);border-bottom:1px solid rgba(244,189,63,.5);backdrop-filter:blur(6px)}}
[data-theme="light"] .site-bar{{background:rgba(255,255,255,.94);border-bottom-color:#c9a227}}
.site-bar .ttl{{color:var(--gold);font-weight:800;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
[data-theme="light"] .site-bar .ttl,[data-theme="light"] .site-bar button,[data-theme="light"] .lang a[aria-current]{{color:#7a5a00;border-color:#7a5a00}}
.site-bar nav{{display:flex;align-items:center;gap:10px;flex:0 0 auto}}
.lang a{{color:var(--fg);opacity:.6;text-decoration:none;font-weight:700;font-size:16px;padding:2px 4px}}
.lang a[aria-current]{{opacity:1;color:var(--gold)}} .lang span{{opacity:.4}}
.site-bar button{{font:700 16px system-ui,sans-serif;color:var(--gold);background:transparent;border:1px solid var(--gold);border-radius:4px;padding:4px 12px;cursor:pointer}}
.intro{{max-width:{maxw};margin:18px auto 8px;padding:0 5mm}}
.intro h1{{font-size:20px;margin:0 0 4px}} .intro p{{margin:0;color:var(--muted);font-size:16px}}
.intro a{{color:var(--gold)}} [data-theme="light"] .intro a{{color:#7a5a00}}
.slide{{display:block;max-width:{maxw};margin:0 auto 26px;padding:0 5mm;scroll-margin-top:64px}}
.fit{{position:relative;width:100%;aspect-ratio:{ratio};overflow:hidden;background:#06152d;border-radius:4px;box-shadow:0 6px 24px rgba(0,0,0,.35);cursor:pointer}}
.fit .blur{{position:absolute;inset:-4%;filter:blur(18px) brightness(.8) saturate(.9);transform:scale(1.05)}}
.fit iframe{{position:absolute;left:0;top:0;border:0;transform-origin:0 0;pointer-events:none;background:transparent}}
.fit.is-empty .blur{{display:none}}
.credit{{margin:6px 0 0;font-size:11px;font-style:italic;color:var(--muted);text-align:right}}
.credit a{{color:inherit}}
.imgtools{{position:absolute;right:12px;top:12px;z-index:30;display:flex;gap:8px}} .imgtools[hidden]{{display:none}}
.imgtools button{{font:700 14px system-ui,sans-serif;padding:6px 14px;border:1.5px solid var(--gold);background:rgba(6,21,45,.9);color:var(--gold);border-radius:4px;cursor:pointer}}
.narr-btn{{position:absolute;right:12px;bottom:12px;z-index:30;width:40px;height:40px;border-radius:50%;border:1.5px solid var(--gold);background:rgba(6,21,45,.85);color:var(--gold);font-size:16px;cursor:pointer}}
html[data-record] .site-bar,html[data-record] .intro,html[data-record] .narr-btn,html[data-record] .imgtools{{display:none!important}}
"""

JS_FIT = """<script>
(function(){
  function fit(){ document.querySelectorAll('.fit').forEach(function(b){ var f=b.querySelector('iframe'); var s=b.clientWidth/(+b.dataset.w);
    f.style.transform='scale('+s+')'; }); }
  addEventListener('resize', fit); fit();
})();
</script>"""

JS_TOOLS = r"""<script>
(function(){
  var P = '__P__', mem = {};
  if(/[?&]record\b/.test(location.search)) document.documentElement.setAttribute('data-record','1');
  function lsGet(k){ try{ return localStorage.getItem(P+k); }catch(e){ return mem[k]||null; } }
  function lsSet(k,v){ mem[k]=v; try{ if(v===null) localStorage.removeItem(P+k); else localStorage.setItem(P+k,v); }catch(e){} }
  var root=document.documentElement; root.setAttribute('data-theme', lsGet('theme')||'dark');
  var tb=document.getElementById('theme-btn');
  function label(){ tb.textContent = root.getAttribute('data-theme')==='light' ? '__DARK__' : '__LIGHT__'; }
  label(); tb.addEventListener('click', function(){ var t=root.getAttribute('data-theme')==='light'?'dark':'light'; root.setAttribute('data-theme',t); lsSet('theme',t); label(); });
  var db=null;
  try{ var rq=indexedDB.open('HormuzDB',1); rq.onupgradeneeded=function(){ rq.result.createObjectStore('media'); };
    rq.onsuccess=function(){ db=rq.result; restore(); }; rq.onerror=function(){ restore(); }; }catch(e){ restore(); }
  function idbPut(k,v){ if(!db) return; try{ var t=db.transaction('media','readwrite'); if(v===null) t.objectStore('media').delete(P+k); else t.objectStore('media').put(v,P+k); }catch(e){} }
  function idbGet(k,cb){ if(!db) return cb(null); try{ var r=db.transaction('media').objectStore('media').get(P+k); r.onsuccess=function(){cb(r.result||null)}; r.onerror=function(){cb(null)}; }catch(e){ cb(null); } }
  function swap(holder, url, isVid, doc){
    var old=holder.querySelector('[data-media]'); if(!old) return;
    var el=doc.createElement(isVid?'video':'img'); el.setAttribute('data-media',''); el.style.cssText=old.style.cssText;
    if(isVid){ el.autoplay=true; el.muted=true; el.loop=true; el.playsInline=true; } el.src=url; old.replaceWith(el);
  }
  function apply(box, rec){
    if(!rec) return; var f=box.querySelector('iframe'); var go=function(){
      var d=f.contentDocument; if(!d) return; var m=d.querySelector('[data-media]');
      if(rec.deleted){ if(m) m.style.visibility='hidden'; box.classList.add('is-empty'); return; }
      var url=rec.blob?URL.createObjectURL(rec.blob):rec.data; if(!url) return; var v=rec.type&&rec.type.indexOf('video')===0;
      if(m) swap(m.parentNode, url, v, d); var b=box.querySelector('.blur'); if(b) swap(b, url, v, document); box.classList.remove('is-empty'); };
    if(f.contentDocument && f.contentDocument.readyState==='complete') go(); else f.addEventListener('load', go, {once:true});
  }
  function restore(){ document.querySelectorAll('.mbox').forEach(function(box){ var k=box.dataset.mkey;
    idbGet(k,function(r){ if(r) return apply(box,r); var s=lsGet('m_'+k); if(s){ try{ apply(box,JSON.parse(s)); }catch(e){} } }); }); }
  document.querySelectorAll('.mbox').forEach(function(box){
    var tools=box.querySelector('.imgtools'), inp=box.querySelector('input[type=file]'), k=box.dataset.mkey;
    box.addEventListener('click', function(e){ if(e.target.closest('.imgtools,.narr-btn')) return; tools.hidden=!tools.hidden; });
    box.querySelector('.btn-rep').addEventListener('click', function(e){ e.stopPropagation(); inp.click(); });
    inp.addEventListener('change', function(){ var fl=inp.files[0]; if(!fl) return; var rec={type:fl.type, blob:fl}; apply(box,rec); idbPut(k,rec);
      if(fl.size<3e6){ var fr=new FileReader(); fr.onload=function(){ lsSet('m_'+k, JSON.stringify({type:fl.type,data:fr.result})); }; fr.readAsDataURL(fl); }
      tools.hidden=true; });
    box.querySelector('.btn-del').addEventListener('click', function(e){ e.stopPropagation(); var rec={deleted:true}; apply(box,rec); idbPut(k,rec); lsSet('m_'+k, JSON.stringify(rec)); tools.hidden=true; });
  });
})();
</script>""".replace("__P__", f"HormuzMedia2026__ep01_{PLAT}_{LANG}__").replace("__DARK__", UI["dark"]).replace("__LIGHT__", UI["light"])

SCRIPT = open(os.path.join(os.path.dirname(__file__), "template_v2.js"), encoding="utf-8").read()
SCRIPT = SCRIPT.replace("// 자막(캡션)이 먼저 보이고, 내레이션은 0.5초 뒤에 시작한다.", "// caption first; narration 0.5 s later")
SCRIPT = SCRIPT.replace("// 내레이션이 끝나면 다음 페이지로 자동 스크롤 → 다음 페이지 내레이션 자동 재생", "// narration ends → scroll to next slide → its narration starts")

page_title = f"{T['title']} · {PLAT_NAME[PLAT]}"
doc = f"""<!DOCTYPE html>
<html lang="{UI['html_lang']}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(page_title)}</title>
<meta name="description" content="{E(T['desc'])}">
<meta property="og:type" content="video.other">
<meta property="og:title" content="{E(page_title)}">
<meta property="og:description" content="{E(T['desc'])}">
<meta property="og:image" content="{RAW}/imgs/main/novel/ep01/{"ep01_cover.jpg" if LANG == "ko" else "ep01_og_" + LANG + ".jpg"}">
<meta property="og:video" content="{MP4URL}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>{CSS}</style>
</head>
<body>
<header class="site-bar"><span class="ttl">{E(page_title)}</span>
<nav>{nav()}
<button type="button" id="theme-btn">{E(UI['light'])}</button></nav></header>
<section class="intro"><h1>{E(PLAT_NAME[PLAT])} · {W}×{H}</h1><p>{E(T['fiction'])} · <a href="{MP4URL}" target="_blank" rel="noopener">{E(T['mp4'])}</a></p></section>
{''.join(parts)}
{JS_FIT}
{SCRIPT}
{JS_TOOLS}
</body>
</html>
"""
os.makedirs(OUTDIR, exist_ok=True)
out = f"{OUTDIR}/epic_fury_ep01_{PLAT}_{LANG}.html"
open(out, "w", encoding="utf-8").write(doc)
print("wrote", out, len(doc))
