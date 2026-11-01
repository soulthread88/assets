# -*- coding: utf-8 -*-
"""EP01 blog posts — Tistory / Naver / WordPress / Substack × ko / en / jp.
Each file is a preview page (site menu, 30:9 hero, left text box + right 16:9 media box with click-to-show
replace/delete) plus a "copy" button that copies the platform-ready body (inline styles, no scripts).
Images, clips and videos load from GitHub (soulthread88). Usage: python3 make_blogs.py OUTDIR"""
import os, sys, json, html, importlib
sys.path.insert(0, os.path.dirname(__file__))
E = html.escape
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
RAW = "https://raw.githubusercontent.com/soulthread88"
MEDIA_LFS = "https://media.githubusercontent.com/media/soulthread88"
MAN = json.load(open("/home/claude/work/media/manifest.json"))
AUTHOR_FIX = {"img_b2_prep": "U.S. Air Force (DVIDS)", "img_ford_deck": "U.S. Navy (DVIDS)",
              "img_spruance": "U.S. Navy · NAVCENT Public Affairs", "img_map100h": "U.S. Department of War"}
HERO = None
HERO_OF = lambda lang: f"{RAW}/imgs/main/novel/ep01/ep01_hero_{lang}.jpg"
LOCAL_OUT = {"ko": "out2", "en": "out_en", "jp": "out_jp"}

def murl(k):
    m = MAN[k]
    if m["type"] == "video": return f"{RAW}/videos/main/novel/ep01/platform_ko/source/{m['file']}"
    return f"{RAW}/imgs/main/novel/ep01/platform_ko/{m['file']}"

def poster(k):
    """Still image for a clip (used where a platform strips <video>): the episode's own thumbnails."""
    m = MAN[k]
    return murl(k) if m["type"] != "video" else HERO

def mp4(lang, plat):
    f = f"epic_fury_ep01_{plat}_{lang}.mp4"; loc = f"/home/claude/work/{LOCAL_OUT[lang]}/{f}"
    big = (not os.path.exists(loc) and plat == "longform") or (os.path.exists(loc) and os.path.getsize(loc) > 95e6)
    return f"{MEDIA_LFS if big else RAW}/videos/main/novel/ep01/platform_{lang}/{f}"

def credit_txt(k):
    m = MAN[k]; return f"{AUTHOR_FIX.get(k, m.get('author') or '')} · {m.get('license') or ''} · {m['site']}", m["page"]

L10N = {
 "ko": dict(mod="content_v2", html_lang="ko", series="장대한 분노 · 호르무즈의 밤", ep="제1화", sit="소설 속 전쟁 상황 속보",
            watch="영상으로 보기", longform="롱폼 영상(약 9분)", shorts="쇼츠(2분 속보)", read="전체 소설 페이지(내레이션)",
            fiction="이 글은 2026년 2월 28일의 실제 사건에서 착상한 소설입니다. 등장인물과 대화는 창작이며, 뉴스 부분의 수치는 당시 보도를 바탕으로 했습니다.",
            credits="사진·영상 출처", next="2화에서 계속됩니다.", copy="본문 복사", copied="복사했습니다",
            tags=["장대한분노", "호르무즈의밤", "전쟁소설", "연재소설", "이란전쟁", "웹소설"],
            lede="모든 전쟁은 누군가의 아침에서 시작되었다. 테헤란의 노교수, 펜타곤의 작전부장, 포드함 함장, CIA 분석관, 그리고 잔해 아래의 일곱 살 아이 — 개전 첫날 아침을 다섯 개의 시선으로 따라갑니다.",
            nav="블로그", light="☀ Light", dark="🌙 Dark", rep="교체", dele="삭제"),
 "en": dict(mod="content_en", html_lang="en", series="Epic Fury: Night Over Hormuz", ep="Episode 1", sit="Situation report (fiction)",
            watch="Watch", longform="Longform video (about 10 min)", shorts="Shorts (2-minute bulletin)", read="Full narrated novel page",
            fiction="This is a novel inspired by real events of Feb. 28, 2026. Characters and dialogue are invented; figures in the news sections follow reporting at the time.",
            credits="Photo and video credits", next="Continued in Episode 2.", copy="Copy post body", copied="Copied",
            tags=["EpicFury", "NightOverHormuz", "WarNovel", "SerialFiction", "IranWar", "MilitaryThriller"],
            lede="Every war begins on somebody’s morning. An old professor in Tehran, the Pentagon’s operations chief, the captain of the USS Gerald R. Ford, a CIA analyst and a 7-year-old girl under the rubble: the first morning of the war through five sets of eyes.",
            nav="Blog", light="☀ Light", dark="🌙 Dark", rep="Replace", dele="Delete"),
 "jp": dict(mod="content_jp", html_lang="ja", series="エピック・フューリー：ホルムズの夜", ep="第1話", sit="作中の戦況速報",
            watch="動画で見る", longform="ロングフォーム動画（約12分）", shorts="ショート（2分の速報）", read="ナレーション付き小説ページ",
            fiction="この作品は2026年2月28日の実際の出来事に着想を得た小説です。登場人物と会話は創作で、ニュース部分の数字は当時の報道に基づいています。",
            credits="写真・動画のクレジット", next="第2話へ続く。", copy="本文をコピー", copied="コピーしました",
            tags=["エピックフューリー", "ホルムズの夜", "戦争小説", "連載小説", "イラン戦争", "Web小説"],
            lede="すべての戦争は、誰かの朝に始まった。テヘランの老教授、国防総省の作戦部長、空母フォードの艦長、CIAの分析官、そしてがれきの下の七歳の少女。開戦初日の朝を、五つのまなざしで追います。",
            nav="ブログ", light="☀ ライト", dark="🌙 ダーク", rep="差し替え", dele="削除"),
}
PLAT = {"tistory": "Tistory", "naver": "Naver Blog", "wordpress": "WordPress", "substack": "Substack"}
F = {"ko": "'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif", "en": "Georgia,'Times New Roman',serif",
     "jp": "'Noto Sans JP','Hiragino Sans','Yu Gothic',Meiryo,sans-serif"}

def body(lang, plat):
    """Platform-ready post body: only inline styles, no scripts."""
    global HERO; HERO = HERO_OF(lang)
    T = L10N[lang]; K = importlib.import_module(T["mod"])
    title = f"{T['series']} — {T['ep']}{':' if lang == 'en' else ''} {K.SUBTITLE}"
    p = lambda t, st="": f'<p style="margin:0 0 1.1em;line-height:1.8;font-size:17px{";" + st if st else ""}">{E(t)}</p>'
    def fig(k, cap=None):
        m = MAN[k]; c, page = credit_txt(k)
        cr = f'<figcaption style="font-size:12px;font-style:italic;color:#666;text-align:right;margin-top:4px">{E(cap + " · " if cap else "")}<a href="{E(page)}" style="color:#666">{E(c)}</a></figcaption>'
        if m["type"] == "video" and plat in ("tistory", "wordpress"):
            inner = (f'<video src="{murl(k)}" poster="{HERO}" autoplay muted loop playsinline controls '
                     f'style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block"></video>')
        elif m["type"] == "video":
            inner = f'<a href="{murl(k)}"><img src="{HERO}" alt="{E(cap or "")}" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block"></a>'
        else:
            inner = f'<img src="{murl(k)}" alt="{E(cap or "")}" style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block">'
        f_ = f'<figure style="margin:1.4em 0">{inner}{cr}</figure>'
        if plat == "wordpress":
            return f"<!-- wp:html -->\n{f_}\n<!-- /wp:html -->"
        return f_
    def video_block():
        lf, sh = mp4(lang, "longform"), mp4(lang, "shorts")
        page = f"{RAW.replace('raw.githubusercontent.com', 'github.com')}/htmls/blob/main/novel/epic_fury_ep01_longform_{lang}.html"
        links = (f'<p style="margin:.6em 0 1.4em;font-size:16px">▶ <a href="{lf}">{E(T["longform"])}</a> · '
                 f'<a href="{sh}">{E(T["shorts"])}</a> · <a href="{page}">{E(T["read"])}</a></p>')
        if plat in ("tistory", "wordpress"):
            v = f'<video src="{lf}" poster="{HERO}" controls playsinline preload="metadata" style="width:100%;aspect-ratio:16/9;background:#000;display:block"></video>'
            v = f"<!-- wp:html -->\n{v}\n<!-- /wp:html -->" if plat == "wordpress" else v
            return f'<h2 style="font-size:22px;margin:1.6em 0 .6em">{E(T["watch"])}</h2>{v}{links}'
        return (f'<h2 style="font-size:22px;margin:1.6em 0 .6em">{E(T["watch"])}</h2>'
                f'<a href="{lf}"><img src="{HERO}" alt="{E(T["longform"])}" style="width:100%;aspect-ratio:30/9;object-fit:cover;display:block"></a>{links}')
    out = []
    out.append(f'<img src="{HERO}" alt="{E(title)}" style="width:100%;aspect-ratio:30/9;object-fit:cover;display:block;margin:0 0 1.2em">')
    out.append(p(T["lede"], "font-size:18px;font-weight:600"))
    out.append(f'<p style="margin:0 0 1.6em;font-size:14px;color:#777;font-style:italic">{E(T["fiction"])}</p>')
    out.append(video_block())
    out.append(f'<h2 style="font-size:22px;margin:1.6em 0 .6em">{E(T["sit"])}</h2>')
    for pg in K.PAGES[:5]:
        out.append(f'<h3 style="font-size:17px;margin:1.2em 0 .3em;color:#b8860b">{E(pg["loc"])}</h3>')
        out.append(p(pg["text"]))
        if pg["n"] in (1, 2, 5): out.append(fig(pg["media"], pg["loc"]))
    for j in range(8):
        a, b = K.PAGES[5 + 2 * j], K.PAGES[6 + 2 * j]
        out.append(f'<h2 style="font-size:22px;margin:1.8em 0 .2em">{E(a["h2"])}</h2>')
        out.append(f'<p style="margin:0 0 .9em;font-size:14px;color:#b8860b;font-weight:700">{E(a["tag"])}</p>')
        out.append(fig(a["media"], a["h2"]))
        out.append(p(a["text"])); out.append(p(b["text"]))
    out.append(f'<p style="margin:1.6em 0;font-weight:800;color:#b8860b">{E(K.END_NOTE)}</p>')
    cr = []
    seen = []
    for pg in K.PAGES:
        if pg["media"] not in seen: seen.append(pg["media"])
    for k in seen:
        c, page = credit_txt(k); cr.append(f'<li><a href="{E(page)}">{E(c)}</a></li>')
    out.append(f'<h3 style="font-size:15px;margin:1.6em 0 .4em">{E(T["credits"])}</h3><ul style="font-size:13px;font-style:italic;color:#666;line-height:1.7">{"".join(cr)}</ul>')
    out.append(f'<p style="font-size:14px;color:#777">{" ".join("#" + E(t) for t in T["tags"])}</p>')
    if plat == "wordpress":
        wrapped = []
        for x in out:
            if x.startswith("<!-- wp:"): wrapped.append(x)
            elif x.startswith("<h2"): wrapped.append(f"<!-- wp:heading -->\n{x}\n<!-- /wp:heading -->")
            elif x.startswith("<h3"): wrapped.append(f'<!-- wp:heading {{"level":3}} -->\n{x}\n<!-- /wp:heading -->')
            elif x.startswith("<p"): wrapped.append(f"<!-- wp:paragraph -->\n{x}\n<!-- /wp:paragraph -->")
            else: wrapped.append(f"<!-- wp:html -->\n{x}\n<!-- /wp:html -->")
        out = wrapped
    return title, "\n".join(out)

def nav(lang, plat):
    items = [("ko", "Kor", "ko"), ("en", "Eng", "en"), ("jp", "Jpn", "ja")]
    return '<span class="lang">' + ' <span>|</span> '.join(
        f'<a href="epic_fury_ep01_blog_{plat}_{c}.html"{" aria-current=\"page\"" if c == lang else ""} lang="{hl}">{lab}</a>' for c, lab, hl in items) + '</span>'

def preview(lang, plat):
    global HERO
    T = L10N[lang]; K = importlib.import_module(T["mod"])
    title, b = body(lang, plat)
    # preview sections: left text box, right 16:9 media box (centred vertically), media tools on click
    secs = []
    for j in range(8):
        a, c = K.PAGES[5 + 2 * j], K.PAGES[6 + 2 * j]; k = a["media"]; m = MAN[k]; cr, page = credit_txt(k)
        el = (f'<video data-media autoplay muted loop playsinline src="{murl(k)}"></video>' if m["type"] == "video"
              else f'<img data-media alt="" src="{murl(k)}">')
        secs.append(f'<section class="row"><div class="txt"><p class="tag">{E(a["tag"])}</p><h2>{E(a["h2"])}</h2>'
                    f'<p>{E(a["text"])}</p><p>{E(c["text"])}</p></div>'
                    f'<figure class="mbox" data-mkey="s{j}"><div class="box">{el}<div class="imgtools" hidden><button type="button" class="btn-rep">{E(T["rep"])}</button>'
                    f'<button type="button" class="btn-del">{E(T["dele"])}</button><input type="file" accept="image/*,video/*" hidden></div></div>'
                    f'<figcaption><a href="{E(page)}" target="_blank" rel="noopener">{E(cr)}</a></figcaption></figure></section>')
    css = f"""
:root{{--bg:#020914;--fg:#f7f8fa;--muted:rgba(247,248,250,.7);--gold:#f4bd3f;--card:#06152d}}
:root[data-theme="light"]{{--bg:#f4f5f7;--fg:#101828;--muted:#475467;--gold:#8a6400;--card:#fff}}
*{{box-sizing:border-box}} html,body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.75 {F[lang]}}}
.site-bar{{position:sticky;top:0;z-index:50;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 5mm;background:var(--card);border-bottom:1px solid var(--gold)}}
.site-bar .ttl{{color:var(--gold);font-weight:800;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.site-bar nav{{display:flex;gap:10px;align-items:center;flex:0 0 auto}}
.lang a{{color:var(--fg);opacity:.6;text-decoration:none;font-weight:700}} .lang a[aria-current]{{opacity:1;color:var(--gold)}} .lang span{{opacity:.4}}
.site-bar button,.copy{{font:700 16px system-ui,sans-serif;color:var(--gold);background:transparent;border:1px solid var(--gold);border-radius:4px;padding:4px 12px;cursor:pointer}}
.hero{{width:100%;aspect-ratio:30/9;object-fit:cover;display:block}}
main{{max-width:1180px;margin:0 auto;padding:16px 0 40px}}
.head{{padding:0 5mm}} .head h1{{font-size:28px;line-height:1.3;margin:.6em 0 .3em}} .head .lede{{font-size:18px}} .head .fic{{color:var(--muted);font-style:italic;font-size:16px}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:center;padding:22px 5mm;border-top:1px solid rgba(244,189,63,.25)}}
.txt .tag{{color:var(--gold);font-weight:700;font-size:16px;margin:0}} .txt h2{{margin:.1em 0 .4em;font-size:24px}} .txt p{{margin:0 0 .8em}}
.mbox{{margin:0;cursor:pointer}} .box{{position:relative;aspect-ratio:16/9;overflow:hidden;background:#06152d;border-radius:4px}}
.box img,.box video{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.mbox.is-empty [data-media]{{visibility:hidden}}
figcaption{{font-size:11px;font-style:italic;color:var(--muted);text-align:right;margin-top:4px}} figcaption a{{color:inherit}}
.imgtools{{position:absolute;right:10px;top:10px;display:flex;gap:8px;z-index:3}} .imgtools[hidden]{{display:none}}
.imgtools button{{font:700 14px system-ui,sans-serif;padding:6px 14px;border:1.5px solid var(--gold);background:rgba(6,21,45,.9);color:#f4bd3f;border-radius:4px;cursor:pointer}}
.export{{margin:28px 5mm 0;padding:16px;border:1px dashed var(--gold);border-radius:6px}}
.export h2{{font-size:18px;margin:0 0 8px}} .export textarea{{width:100%;height:160px;font:13px/1.5 ui-monospace,monospace;background:var(--card);color:var(--fg);border:1px solid var(--muted)}}
@media(max-width:820px){{.row{{grid-template-columns:1fr}} .head h1{{font-size:22px}}}}
"""
    js = r"""<script>
// still here. still counting.
(function(){
  var P='__P__', mem={};
  function g(k){ try{ return localStorage.getItem(P+k); }catch(e){ return mem[k]||null; } }
  function s(k,v){ mem[k]=v; try{ if(v===null) localStorage.removeItem(P+k); else localStorage.setItem(P+k,v); }catch(e){} }
  var r=document.documentElement; r.setAttribute('data-theme', g('theme')||'dark');
  var tb=document.getElementById('theme-btn'); function lab(){ tb.textContent = r.getAttribute('data-theme')==='light' ? '__DARK__' : '__LIGHT__'; }
  lab(); tb.onclick=function(){ var t=r.getAttribute('data-theme')==='light'?'dark':'light'; r.setAttribute('data-theme',t); s('theme',t); lab(); };
  var db=null; try{ var q=indexedDB.open('HormuzDB',1); q.onupgradeneeded=function(){ q.result.createObjectStore('media'); };
    q.onsuccess=function(){ db=q.result; restore(); }; q.onerror=restore; }catch(e){ restore(); }
  function put(k,v){ if(!db) return; try{ var t=db.transaction('media','readwrite'); t.objectStore('media').put(v,P+k); }catch(e){} }
  function get(k,cb){ if(!db) return cb(null); try{ var q=db.transaction('media').objectStore('media').get(P+k); q.onsuccess=function(){cb(q.result||null)}; q.onerror=function(){cb(null)}; }catch(e){ cb(null); } }
  function apply(f,rec){ if(!rec) return; if(rec.deleted){ f.classList.add('is-empty'); return; }
    var u=rec.blob?URL.createObjectURL(rec.blob):rec.data; if(!u) return; var o=f.querySelector('[data-media]'); var v=rec.type&&rec.type.indexOf('video')===0;
    var e=document.createElement(v?'video':'img'); e.setAttribute('data-media',''); if(v){ e.autoplay=e.muted=e.loop=e.playsInline=true; } e.src=u; o.replaceWith(e); f.classList.remove('is-empty'); }
  function restore(){ document.querySelectorAll('.mbox').forEach(function(f){ var k=f.dataset.mkey; get(k,function(x){ if(x) return apply(f,x); var t=g('m_'+k); if(t){ try{ apply(f,JSON.parse(t)); }catch(e){} } }); }); }
  document.querySelectorAll('.mbox').forEach(function(f){ var tl=f.querySelector('.imgtools'), i=f.querySelector('input'), k=f.dataset.mkey;
    f.querySelector('.box').addEventListener('click',function(e){ if(e.target.closest('.imgtools')) return; tl.hidden=!tl.hidden; });
    f.querySelector('.btn-rep').onclick=function(e){ e.stopPropagation(); i.click(); };
    i.onchange=function(){ var x=i.files[0]; if(!x) return; var rec={type:x.type,blob:x}; apply(f,rec); put(k,rec);
      if(x.size<3e6){ var fr=new FileReader(); fr.onload=function(){ s('m_'+k, JSON.stringify({type:x.type,data:fr.result})); }; fr.readAsDataURL(x); } tl.hidden=true; };
    f.querySelector('.btn-del').onclick=function(e){ e.stopPropagation(); var rec={deleted:true}; apply(f,rec); put(k,rec); s('m_'+k, JSON.stringify(rec)); tl.hidden=true; };
  });
  var cb=document.getElementById('copy'); cb.onclick=function(){ var t=document.getElementById('src'); t.select();
    (navigator.clipboard?navigator.clipboard.writeText(t.value):Promise.reject()).catch(function(){ try{ document.execCommand('copy'); }catch(e){} });
    cb.textContent='__COPIED__'; };
})();
</script>""".replace("__P__", f"HormuzMedia2026__ep01_blog_{plat}_{lang}__").replace("__DARK__", T["dark"]).replace("__LIGHT__", T["light"]).replace("__COPIED__", T["copied"])
    return f"""<!DOCTYPE html>
<html lang="{T['html_lang']}" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(title)} · {PLAT[plat]}</title>
<meta name="description" content="{E(T['lede'])}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(T['lede'])}"><meta property="og:image" content="{HERO}">
<style>{css}</style>
</head>
<body>
<header class="site-bar"><span class="ttl">{E(PLAT[plat])} · {E(title)}</span><nav>{nav(lang, plat)}<button type="button" id="theme-btn">{E(T['light'])}</button></nav></header>
<img class="hero" src="{HERO}" alt="">
<main>
<div class="head"><h1>{E(title)}</h1><p class="lede">{E(T['lede'])}</p><p class="fic">{E(T['fiction'])}</p></div>
{''.join(secs)}
<section class="export"><h2>{E(PLAT[plat])} — {E(T['copy'])}</h2><button type="button" class="copy" id="copy">{E(T['copy'])}</button>
<textarea id="src" readonly>{E(b)}</textarea></section>
</main>
{js}
</body>
</html>
"""

for lang in ("ko", "en", "jp"):
    for plat in PLAT:
        f = f"{OUT}/epic_fury_ep01_blog_{plat}_{lang}.html"
        open(f, "w", encoding="utf-8").write(preview(lang, plat))
        print("wrote", f)
