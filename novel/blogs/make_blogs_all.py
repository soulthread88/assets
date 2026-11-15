# -*- coding: utf-8 -*-
"""EPIC FURY EP01~EP10 블로그 일괄 생성(GEO).
입력: 원고 HTML(src/epNN_{final,en,jp}.html), 4K 무료 자료 목록(media4k.json), 자료 출처(media_epNN/manifest.json).
출력: out/epNN/epic_fury_epNN_blog_{naver,tistory,wordpress,substack}_{ko,en,jp}[_body].html
      네이버·티스토리 = KO, 워드프레스·서브스택 = KO·EN·JP.
규칙: 이미지·영상은 3840x2160 이상 무료 자료만, 출처는 박스 바로 아래 작은 기울임 글씨 '출처: …'."""
import json, re, os, sys, html, subprocess
from bs4 import BeautifulSoup
E = html.escape
W = "/home/claude/work"; B = f"{W}/blogs"
IMG = "https://raw.githubusercontent.com/soulthread88/imgs/main/novel/ep{N}/blog/"
VID = "https://media.githubusercontent.com/media/soulthread88/videos/main/novel/ep{N}/platform_{L}/"
POSTED = "2026-11-15"
M4K = json.load(open(f"{B}/media4k.json"))
TITLE_FIX = {("01", "ko"): ("성벽이 무너지는 날", "성벽이 무너진 날"), ("01", "jp"): ("城壁が崩れる日", "城壁が崩れた日")}
LBL = {
 "ko": dict(series="장대한 분노", sub="호르무즈의 밤", ep="제{n}화", novel="(2026 이란 전쟁 소설)", tldr="한눈에 보기 — 제{n}화 핵심 요약", nums="숫자로 보는 제{n}화",
            cols=("항목", "수치", "기준"), tl="제{n}화 주요 사건 타임라인", vid="영상으로 보기", body="제{n}화 「{t}」 본문", scene="장면", intel="기밀 문서 — {t}",
            fact="무엇이 사실이고 무엇이 창작인가", chars="등장인물 현황 — 제{n}화 끝", faq="자주 묻는 질문 (FAQ)", next="다음 화 예고", src="출처", srcw="출처",
            end="— {n}화 끝. {m}화에서 계속됩니다. —", fiction="소설은 이 날들을 {who}의 눈으로 따라간다. 등장인물과 대화는 창작이다.",
            q_what="「장대한 분노」 제{n}화는 어떤 내용인가요?", q_who="{t}은(는) 무엇인가요?", q_true="이 소설은 실화인가요?",
            a_true="아닙니다. 공개 보도로 확인되는 사실을 뼈대로 삼은 픽션입니다. {who} 같은 인물과 모든 대화, 기밀 문서는 창작입니다.",
            q_vid="영상으로도 볼 수 있나요?", a_vid="네. {list} 영상이 있고, 한국어·영어·일본어 내레이션과 자막이 있습니다.",
            disc="이 소설은 2026년 2월 28일 개시된 미국·이스라엘의 대이란 군사작전(Operation Epic Fury)과 그 이후의 전쟁에서 착상을 얻은 픽션입니다. 등장인물, 대화, 내면, 기밀 문서는 모두 창작이며, 실존 인물에게 부여된 발언과 판단 역시 지어낸 것입니다. 사실 보도나 정세 분석용이 아닙니다.",
            vids=dict(longform="유튜브·페이스북 롱폼 4K", shorts="유튜브 쇼츠", reels="인스타그램 릴스", tiktok="틱톡", threads="스레드", x="X", facebook="페이스북", feeds="인스타그램 피드"),
            and_="·", font="Noto+Sans+KR", fam="'Noto Sans KR'"),
 "en": dict(series="Epic Fury", sub="Night Over Hormuz", ep="Episode {n}", novel="(A Novel of the 2026 Iran War)", tldr="At a Glance — Episode {n} in Brief", nums="Episode {n} in Numbers",
            cols=("Item", "Figure", "Note"), tl="Episode {n} Timeline", vid="Watch", body="Episode {n}, “{t}”", scene="Scene", intel="Classified — {t}",
            fact="What Is Fact and What Is Fiction", chars="Characters at the End of Episode {n}", faq="Frequently Asked Questions", next="Next Episode", src="Sources", srcw="Source",
            end="— End of Episode {n}. Continued in Episode {m}. —", fiction="The novel follows these days through the eyes of {who}. Characters and dialogue are fiction.",
            q_what="What is Epic Fury Episode {n} about?", q_who="What is {t}?", q_true="Is this novel a true story?",
            a_true="No. It is fiction built on facts confirmed by public reporting. Characters such as {who}, and all dialogue and classified documents, are invented.",
            q_vid="Can I watch it as a video?", a_vid="Yes. There are {list} videos, with Korean, English and Japanese narration and subtitles.",
            disc="This novel is a work of fiction inspired by the U.S.–Israeli military operation against Iran (Operation Epic Fury) launched on February 28, 2026, and the war that followed. Characters, dialogue, inner thoughts and classified documents are invented, as are the statements attributed to real people. It is not intended as factual reporting or analysis.",
            vids=dict(longform="YouTube and Facebook long form 4K", shorts="YouTube Shorts", reels="Instagram Reels", tiktok="TikTok", threads="Threads", x="X", facebook="Facebook", feeds="Instagram Feed"),
            and_=", ", font="Noto+Sans", fam="'Noto Sans'"),
 "jp": dict(series="壮大なる怒り", sub="ホルムズの夜", ep="第{n}話", novel="（2026年イラン戦争小説）", tldr="ひと目でわかる — 第{n}話の要点", nums="数字で見る第{n}話",
            cols=("項目", "数値", "基準"), tl="第{n}話 主な出来事のタイムライン", vid="動画で見る", body="第{n}話「{t}」本文", scene="場面", intel="機密文書 — {t}",
            fact="何が事実で何が創作か", chars="登場人物の現況 — 第{n}話終了時", faq="よくある質問（FAQ）", next="次回予告", src="出典", srcw="出典",
            end="— 第{n}話 終わり。第{m}話に続く。 —", fiction="小説はこの日々を{who}の目で追う。登場人物と会話は創作である。",
            q_what="「壮大なる怒り」第{n}話はどんな内容ですか？", q_who="{t}とは何ですか？", q_true="この小説は実話ですか？",
            a_true="いいえ。公開報道で確認できる事実を骨組みにしたフィクションです。{who}などの人物、すべての会話と機密文書は創作です。",
            q_vid="動画でも見られますか？", a_vid="はい。{list}の動画があり、韓国語・英語・日本語のナレーションと字幕があります。",
            disc="この小説は、2026年2月28日に始まった米国・イスラエルによる対イラン軍事作戦（Operation Epic Fury）とその後の戦争に着想を得たフィクションです。登場人物、会話、内面、機密文書はすべて創作であり、実在の人物に与えられた発言や判断も創作です。事実報道や情勢分析を目的としたものではありません。",
            vids=dict(longform="YouTube・Facebook 長編 4K", shorts="YouTubeショート", reels="Instagramリール", tiktok="TikTok", threads="Threads", x="X", facebook="Facebook", feeds="Instagramフィード"),
            and_="・", font="Noto+Sans+JP", fam="'Noto Sans JP'"),
}
REAL = re.compile(r"(실존|Real|実在|実際)")
VID_ORDER = ["longform", "shorts", "threads", "x", "reels", "tiktok", "facebook", "feeds"]

def txt(e): return re.sub(r"\s+", " ", e.get_text().strip()) if e is not None else ""

def parse(N, L):
    f = f"{B}/src/ep{N}_{'final' if L == 'ko' else L}.html"
    s = BeautifulSoup(open(f).read(), "html.parser"); g = lambda c: txt(s.select_one(c))
    d = dict(title=g(".chapter-title"), tagline=g(".cover-tagline"), subtitle=g(".chapter-subtitle"), date=g(".cover-date"))
    fx = TITLE_FIX.get((N, L))
    if fx: d["title"] = d["title"].replace(*fx)
    kw = s.find("meta", attrs={"name": "keywords"}); d["kw"] = [x.strip() for x in (kw.get("content") if kw else "").split(",") if x.strip()][:12]
    d["nums"] = [(txt(e.select_one(".wc-label")), txt(e.select_one(".wc-val")), txt(e.select_one(".wc-sub"))) for e in s.select(".wc-item")]
    d["tl"] = [(txt(e.select_one(".ep-tl-time")), txt(e.select_one(".ep-tl-text"))) for e in s.select(".ep-tl-item")]
    it = s.select_one(".intel-intercept")
    d["intel"] = (txt(it.select_one(".intel-subject")), [txt(x) for x in it.select(".intel-text")]) if it else None
    d["inserts"] = [(txt(e.select_one(".insert-label")), txt(e.select_one(".insert-title")), [txt(p) for p in e.find_all("p") if txt(p)]) for e in s.select(".insert")]
    d["chars"] = [(txt(e.select_one(".cs-name")), txt(e.select_one(".cs-role")), txt(e.select_one(".cs-note"))) for e in s.select(".cs-card")]
    d["notes"] = []
    for e in s.select(".anno-item"):
        term = e.select_one(".anno-term"); ty = term.select_one(".anno-type") if term else None
        tytx = txt(ty)
        if ty: ty.extract()
        d["notes"].append((txt(term), tytx, txt(e.select_one(".anno-def"))))
    nx = s.select_one(".next-ep-teaser")
    d["next"] = [txt(nx.select_one(c)) for c in (".next-ep-ep", ".next-ep-place", ".next-ep-teaser-line")] if nx else []
    d["sources"] = []
    for li in s.select(".sources-list li"):
        a = li.select_one("a.src-url, a")
        if not a: continue
        url = a.get("href"); a.extract(); lab = txt(li)
        if re.match(r"^(이미지|Image|画像|장면 요약|Scene summary|場面|영상|Video|動画)", lab): continue
        d["sources"].append((lab, url))
    # 장면
    sc = []; cur = None
    STOP = re.compile(r"(char-status|cs-wrap|anno|next-ep|continues|sources|love-passage)")
    for el in s.find_all(["div", "p", "section"]):
        cls = " ".join(el.get("class") or [])
        if el.name == "div" and "scene" in (el.get("class") or []) and el.select_one(".scene-place"):
            cur = dict(place=txt(el.select_one(".scene-place")), time=txt(el.select_one(".scene-time")), paras=[]); sc.append(cur); continue
        if cur is None: continue
        if el.name in ("div", "section") and STOP.search(cls): cur = None; continue
        if el.name == "p" and not el.find_parent(class_=re.compile(r"image-block|intel|flashnews|cs-card|anno|insert|summary|scene-indicator|share|cover|chapter|war-cost|ep-tl|map")):
            t = txt(el)
            t = re.sub(r"\s*✦\s*(공유|Share|シェア|共有)\s*$", "", t)
            if not t: continue
            c = [x for x in (el.get("class") or []) if x in ("factual", "dialogue", "impact", "shareable")]
            cur["paras"].append((c[0] if c else "", t))
    d["scenes"] = [x for x in sc if x["paras"]]
    return d

def man(N):
    return json.load(open(f"{W}/media_ep{N}/manifest.json" if N != "01" else f"{W}/media/manifest.json"))

BRIGHT = json.load(open(f"{B}/bright.json")) if os.path.exists(f"{B}/bright.json") else {}
def media_keys(N):
    ks = [k for k, w, h, site, ty in M4K[str(int(N))] if not k.startswith("ai_")]
    br = dict(BRIGHT.get(N, []))
    if not br: return ks
    ok = [k for k in ks if br.get(k, 0) >= 60]          # 밝은 화면만(시니어 친화)
    if len(ok) < 6: ok = sorted(ks, key=lambda k: -br.get(k, 0))[:max(6, len(ok))]
    cover = max(ok[:6], key=lambda k: br.get(k, 0))      # 앞쪽 자료 중 가장 밝은 것을 표지로
    return [cover] + [k for k in ok if k != cover]

def credit(m, L):
    return " · ".join(x for x in [m.get("author"), m.get("license"), m.get("site")] if x)

def videos(N, L):
    out = subprocess.run(["git", "-C", "/home/claude/videos", "ls-files", f"novel/ep{N}/platform_{L}/"], capture_output=True, text=True).stdout.split()
    have = {re.sub(rf".*epic_fury_ep{N}_(.*)_{L}\.mp4", r"\1", p) for p in out if p.endswith(f"_{L}.mp4")}
    return [p for p in VID_ORDER if p in have]

def build(N, L, mode):
    n = int(N); t = LBL[L]; d = parse(N, L); MAN = man(N); keys = media_keys(N)
    cover, tlimg = keys[0], keys[1 % len(keys)]
    rest = keys[2:] or keys
    scene_keys = [rest[(i * len(rest)) // max(1, len(d["scenes"]))] for i in range(len(d["scenes"]))]
    IM = IMG.format(N=N); V = VID.format(N=N, L=L)
    who = t["and_"].join(c[0] for c in d["chars"][:4])
    title = f'{t["series"]} {t["ep"].format(n=n)} 「{d["title"]}」 — {d["tagline"]} {t["novel"]}' if L != "en" else f'{t["series"]} {t["ep"].format(n=n)}, “{d["title"]}” — {d["tagline"]} {t["novel"]}'
    desc = f'{d["subtitle"]} ' + ({"ko": f"실제 사건에서 착상한 전쟁 소설 「장대한 분노」 제{n}화의 줄거리, 타임라인, 숫자, 사실과 창작의 구분.",
                                   "en": f"Episode {n} of the war novel Epic Fury: summary, timeline, numbers, and what is fact and what is fiction.",
                                   "jp": f"実際の出来事に着想を得た戦争小説「壮大なる怒り」第{n}話のあらすじ、タイムライン、数字、事実と創作の区別。"}[L])
    vids = videos(N, L)
    faq = [(t["q_what"].format(n=n), d["subtitle"])]
    for term, ty, df in [x for x in d["notes"] if REAL.search(x[1])][:3]:
        faq.append((t["q_who"].format(t=re.sub(r"\s*\(.*?\)\s*$", "", term)), df))
    faq.append((t["q_true"], t["a_true"].format(who=who)))
    if vids: faq.append((t["q_vid"], t["a_vid"].format(list=t["and_"].join(t["vids"][v] for v in vids))))
    st = (lambda k: f' style="{k}"') if mode == "naver" else (lambda k: "")
    S = dict(h2="font-size:26px;line-height:1.4;font-weight:800;color:#0b2245;margin:44px 0 14px;padding-left:14px;border-left:8px solid #e8000f",
             h3="font-size:21px;font-weight:800;color:#c8202d;margin:24px 0 8px", p="margin:0 0 18px",
             cap="font-size:16px;margin:8px 0 2px;font-weight:500", src="font-size:14px;font-style:italic;color:#555;margin:2px 0 0",
             td="padding:10px;border:1px solid #e3dccb;vertical-align:top", th="background:#0b2245;color:#fff;padding:10px;text-align:left")
    h = lambda tag, x: f"<{tag}{st(S[tag])}>{x}</{tag}>"
    CLS = {"dialogue": "dlg", "factual": "fact", "impact": "impact", "shareable": "impact"}
    def p(x, c=""):
        cl = CLS.get(c, "")
        if cl and mode in ("wordpress", "tistory"): return f'<p class="{cl}">{E(x)}</p>'
        if mode == "naver":
            extra = {"fact": "background:#f6f3ec;padding:12px 16px;border-radius:8px;", "impact": "font-weight:800;color:#c8202d;", "dlg": "padding-left:14px;border-left:3px solid #e3dccb;"}.get(cl, "")
            return f'<p style="{extra}margin:0 0 18px">{E(x)}</p>'
        if mode == "substack" and cl == "impact": return f"<blockquote>{E(x)}</blockquote>"
        return f"<p>{E(x)}</p>"
    def fig(k, cap, video=None):
        m = MAN[k]; src = f'{t["srcw"]}: <a href="{E(m["page"])}" target="_blank" rel="noopener"' + (' style="color:#555"' if mode == "naver" else "") + f'>{E(credit(m, L))}</a>'
        url = IM + k + ".jpg"
        if mode == "substack":
            return f'<figure><img src="{url}" alt="{E(cap)}"><figcaption>{E(cap)}<br><em>{src}</em></figcaption></figure>'
        if mode == "naver":
            return (f'<p style="margin:22px 0 4px"><img src="{url}" alt="{E(cap)}" style="width:100%;height:auto;aspect-ratio:16/9;object-fit:cover"></p>'
                    f'<p style="{S["cap"]}">{E(cap)}</p><p style="{S["src"]}"><i>{src}</i></p>')
        media = (f'<video controls preload="metadata" playsinline poster="{url}" src="{video}"></video>' if video
                 else f'<img src="{url}" alt="{E(cap)}" width="3840" height="2160" loading="lazy">')
        return f'<figure>{media}<figcaption><p class="cap">{E(cap)}</p><p class="src"><i>{src}</i></p></figcaption></figure>'
    H = []
    H.append(f'<h1{st("font-size:32px;line-height:1.35;font-weight:900;color:#0b2245;margin:0 0 12px")}>{E(title)}</h1>')
    H.append(f'<p class="meta"{st("font-size:16px;color:#555;margin:0 0 20px")}>{E(t["series"])}: {E(t["sub"])} · {E(d["date"])} · {POSTED}</p>')
    H.append(fig(cover, d["tagline"]))
    tl = [d["subtitle"]] + [b for a, b in d["tl"][:3]] + [t["fiction"].format(who=who)]
    li = "".join(f"<li>{E(x)}</li>" for x in tl)
    H.append(f'<div class="tldr"{st("background:#fff4f4;border:2px solid #e8000f;border-radius:10px;padding:18px 24px;margin:18px 0 28px")}><strong>{E(t["tldr"].format(n=n))}</strong><ul>{li}</ul></div>'
             if mode != "substack" else f"{h('h2', E(t['tldr'].format(n=n)))}<ul>{li}</ul>")
    if d["nums"]:
        H.append(h("h2", E(t["nums"].format(n=n))))
        if mode == "substack": H.append("<ul>" + "".join(f"<li><strong>{E(a)}: {E(b)}</strong> — {E(c)}</li>" for a, b, c in d["nums"]) + "</ul>")
        else: H.append(f'<table{st("width:100%;border-collapse:collapse;font-size:17px")}><thead><tr>' + "".join(f"<th{st(S['th'])}>{E(c)}</th>" for c in t["cols"]) + "</tr></thead><tbody>" +
                       "".join(f"<tr><td{st(S['td'])}>{E(a)}</td><td{st(S['td'])}><b>{E(b)}</b></td><td{st(S['td'])}>{E(c)}</td></tr>" for a, b, c in d["nums"]) + "</tbody></table>")
    if d["tl"]:
        H.append(h("h2", E(t["tl"].format(n=n))))
        for a, b in d["tl"]: H.append(h("h3", E(a)) + p(b))
        H.append(fig(tlimg, d["tl"][min(1, len(d["tl"]) - 1)][1]))
    if vids:
        H.append(h("h2", E(t["vid"])))
        if "longform" in vids and mode in ("wordpress", "tistory"): H.append(fig(cover, t["vids"]["longform"], video=V + f"epic_fury_ep{N}_longform_{L}.mp4"))
        H.append("<ul>" + "".join(f'<li><a href="{V}epic_fury_ep{N}_{v}_{L}.mp4">{E(t["vids"][v])}</a></li>' for v in vids) + "</ul>")
    H.append(h("h2", E(t["body"].format(n=n, t=d["title"]))))
    for i, sc in enumerate(d["scenes"]):
        short = re.split(r"\s*[—―-]\s*", sc["place"])[0] if len(sc["place"]) > 40 else sc["place"]
        H.append(h("h2", f'{E(t["scene"])} {i + 1}. {E(sc["place"])}'))
        intro = f'<p class="time"{st("font-size:15px;color:#555;margin:0 0 14px")}><i>{E(sc["time"])}</i></p>'
        f = fig(scene_keys[i], sc["place"])
        if mode in ("wordpress", "tistory"):
            first = "".join(p(x, c) for c, x in sc["paras"][:2]); rest_ = "".join(p(x, c) for c, x in sc["paras"][2:])
            H.append(f'<div class="row"><div class="col">{intro}{first}</div>{f}</div>{rest_}')
        else: H.append(intro + f + "".join(p(x, c) for c, x in sc["paras"]))
    H.append(p(t["end"].format(n=n, m=n + 1)))
    if d["intel"] and d["intel"][1]:
        H.append(h("h2", E(t["intel"].format(t=d["intel"][0] or "")) ) + "".join(p(x) for x in d["intel"][1]))
    for lab, ti, ps in d["inserts"]:
        if ps: H.append(h("h2", E(f"{ti}" if ti else lab)) + p(lab) * 0 + "".join(p(x) for x in ps))
    if d["notes"]:
        H.append(h("h2", E(t["fact"])))
        for term, ty, df in d["notes"]: H.append(h("h3", E(term + (f" — {ty}" if ty else ""))) + p(df))
    if d["chars"]:
        H.append(h("h2", E(t["chars"].format(n=n))) + "".join(p(f"■ {a} ({b}) — {c}") for a, b, c in d["chars"]))
    H.append(h("h2", E(t["faq"])))
    if mode in ("wordpress", "tistory"): H.append('<dl class="faq">' + "".join(f"<dt>Q. {E(q)}</dt><dd>A. {E(a)}</dd>" for q, a in faq) + "</dl>")
    else:
        for q, a in faq: H.append(h("h3", "Q. " + E(q)) + p("A. " + a))
    if d["next"]: H.append(h("h2", E(t["next"] + " — " + d["next"][0])) + "".join(p(x) for x in d["next"][1:] if x))
    H.append(h("h2", E(t["src"])))
    items = list(d["sources"]); seen = set()
    for k in [cover, tlimg] + scene_keys:
        if k in seen: continue
        seen.add(k); m = MAN[k]
        items.append((f'{m.get("title") or k} — {credit(m, L)}', m["page"]))
    H.append("<ol>" + "".join(f'<li style="overflow-wrap:anywhere">{E(a)}<br><a href="{E(u)}" style="word-break:break-all;overflow-wrap:anywhere">{E(u)}</a></li>' for a, u in items) + "</ol>")
    H.append(f'<div class="disc"{st("font-size:15px;color:#555;background:#f6f3ec;padding:14px 18px;border-radius:8px;margin:24px 0")}>{E(t["disc"])}</div>' if mode != "substack" else f"<p><em>{E(t['disc'])}</em></p>")
    tags = [re.sub(r"\s+", "", k) for k in d["kw"]][:10]
    if mode in ("naver", "tistory"): H.append(f'<p{st("color:#555;font-size:16px")}>' + " ".join("#" + x for x in tags) + "</p>")
    body = "\n".join(H)
    meta = dict(title=title, desc=desc, kw=d["kw"], cover=IM + cover + ".jpg")
    if mode == "substack": return body, meta
    if mode == "naver":
        return (f'<div style="font-family:{t["fam"]},\'Malgun Gothic\',sans-serif;color:#141414;font-size:19px;line-height:1.9;word-break:keep-all;max-width:860px;margin:0 auto">\n{body}\n</div>'), meta
    css = f"""
.efb{{font-family:{t['fam']},sans-serif;color:#141414;font-size:19px;line-height:1.9;word-break:{'normal' if L == 'jp' else 'keep-all'};line-break:strict;max-width:880px;margin:0 auto}}
.efb h1{{font-size:32px;line-height:1.35;font-weight:900;color:#0b2245;margin:0 0 12px}} .efb h2{{{S['h2']}}} .efb h3{{{S['h3']}}} .efb p{{{S['p']}}} .efb .meta{{font-size:16px;color:#555}}
.efb .tldr{{background:#fff4f4;border:2px solid #e8000f;border-radius:10px;padding:18px 24px;margin:18px 0 28px}} .efb .tldr ul{{margin:8px 0 0;padding-left:22px}}
.efb figure{{margin:22px 0 26px}} .efb figure img,.efb figure video{{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:8px;background:#0d0d0d}}
.efb .cap{{{S['cap']}}} .efb .src{{{S['src']}}} .efb .src a{{color:#555}}
.efb table{{width:100%;border-collapse:collapse;margin:10px 0 24px;font-size:17px}} .efb th{{{S['th']}}} .efb td{{{S['td']}}}
.efb .row{{display:flex;gap:28px;align-items:center;flex-wrap:wrap;margin:18px 0 8px}} .efb .row .col{{flex:1 1 380px;min-width:0}} .efb .row figure{{flex:1 1 380px;margin:0}}
.efb .time{{font-size:15px;color:#555}} .efb .dlg{{padding-left:14px;border-left:3px solid #e3dccb}}
.efb .fact{{background:#f6f3ec;padding:12px 16px;border-radius:8px;font-size:17px}} .efb .impact{{font-weight:800;color:#c8202d}}
.efb .faq dt{{font-weight:800;color:#0b2245;margin-top:16px}} .efb .faq dd{{margin:6px 0 0}} .efb .disc{{font-size:15px;color:#555;background:#f6f3ec;padding:14px 18px;border-radius:8px}}
.efb ol li{{margin-bottom:8px}} @media (max-width:640px){{.efb{{font-size:18px}} .efb h1{{font-size:26px}} .efb h2{{font-size:22px}}}}"""
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title[:110], "description": desc, "inLanguage": {"jp": "ja"}.get(L, L), "datePublished": POSTED, "dateModified": POSTED,
         "genre": "War fiction", "image": meta["cover"], "author": {"@type": "Organization", "name": "Epic Fury"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}
    if "longform" in vids:
        ld["@graph"].append({"@type": "VideoObject", "name": t["vids"]["longform"] + " — " + d["title"], "description": desc, "thumbnailUrl": meta["cover"],
                             "uploadDate": POSTED, "contentUrl": V + f"epic_fury_ep{N}_longform_{L}.mp4"})
    return (f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={t["font"]}:wght@400;500;700;800;900&display=swap"><style>{css}</style>\n'
            f'<div class="efb">\n{body}\n</div>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'), meta

def page(L, mode, b, meta):
    t = LBL[L]; lang = {"jp": "ja"}.get(L, L)
    extra = "" if mode in ("wordpress", "tistory") else f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family={t['font']}:wght@400;700;900&display=swap'><style>body{{font-family:{t['fam']},sans-serif;font-size:19px;line-height:1.9;max-width:860px;margin:0 auto;padding:16px}} img{{max-width:100%;height:auto}}</style>"
    return (f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{E(meta['title'])}</title>"
            f"<meta name='description' content='{E(meta['desc'])}'><meta name='keywords' content='{E(', '.join(meta['kw']))}'><meta property='og:title' content='{E(meta['title'])}'>"
            f"<meta property='og:description' content='{E(meta['desc'])}'><meta property='og:image' content='{meta['cover']}'><meta property='og:type' content='article'>{extra}</head>"
            f"<body style='background:#fbf9f4;margin:0;padding:16px'>{b}</body></html>")

JOBS = [("ko", "naver"), ("ko", "tistory"), ("ko", "wordpress"), ("ko", "substack"), ("en", "wordpress"), ("en", "substack"), ("jp", "wordpress"), ("jp", "substack")]
if __name__ == "__main__":
    eps = sys.argv[1:] or [f"{i:02d}" for i in range(1, 11)]
    for N in eps:
        od = f"{B}/out/ep{N}"; os.makedirs(od, exist_ok=True)
        for L, mode in JOBS:
            b, meta = build(N, L, mode); base = f"{od}/epic_fury_ep{N}_blog_{mode}_{L}"
            open(base + ".html", "w").write(page(L, mode, b, meta)); open(base + "_body.html", "w").write(b)
        d = parse(N, "ko")
        print(N, d["title"], "scenes", len(d["scenes"]), [len(s["paras"]) for s in d["scenes"]], "nums", len(d["nums"]), "notes", len(d["notes"]), "vids_ko", videos(N, "ko"))
