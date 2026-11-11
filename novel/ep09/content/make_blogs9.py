# -*- coding: utf-8 -*-
"""EP09 블로그 생성(GEO). Naver·Tistory=KO, WordPress·Substack=KO+EN.
이미지 = 각 장면 4K 영상의 정지 화면(출처는 원 영상), 영상 = 플랫폼 MP4 링크/임베드."""
import json, html, re, os, sys
E = html.escape
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/blog"; os.makedirs(OUT, exist_ok=True)
MAN = json.load(open("/home/claude/work/media_ep09/manifest.json"))
IMG = "https://raw.githubusercontent.com/soulthread88/imgs/main/novel/ep09/"
VID = "https://media.githubusercontent.com/media/soulthread88/videos/main/novel/ep09/platform_{L}/"
POSTED = "2026-11-11"; PLATS = ["longform", "shorts", "tiktok", "reels", "threads", "x", "facebook", "feeds"]
T = {
 "ko": dict(
  title="장대한 분노 제9화 「종이의 여행」 — 미국 15개항 휴전안과 이란의 다섯 조건 (2026 이란 전쟁 소설)",
  desc="2026년 3월 25일, 파키스탄이 미국의 15개항 휴전안을 이란에 전달했고 이란은 거부하며 다섯 조건을 내놓았다. 같은 날 쿠웨이트 공항이 탔다. 실제 사건에서 착상한 전쟁 소설 「장대한 분노」 제9화의 줄거리, 타임라인, 15개항과 5개 조건 비교, 사실과 창작의 구분.",
  meta="연재 소설 「장대한 분노: 호르무즈의 밤」 · 제9화 · 작중 시점 2026년 3월 25일(전쟁 26일째)",
  tldr_h="한눈에 보기 — 제9화 핵심 요약",
  tldr=["3월 25일 파키스탄이 미국의 15개항 휴전안을 이란에 전달했다. 제재 완화를 대가로 핵 프로그램 후퇴, 미사일 제한, 호르무즈 재개방을 요구하는 내용이다.",
        "같은 날 이란 국영 매체는 거부를 보도하고 다섯 조건을 내놓았다: 공격·암살 중단, 재발 방지 보장, 배상, 모든 전선의 종전, 호르무즈 해협 주권.",
        "같은 날 이란 드론이 쿠웨이트 국제공항 연료 저장소를 맞혀 불이 사흘 동안 탔다. 협상과 폭격이 같은 날 함께 왔다.",
        "소설은 이 하루를 파키스탄 외교관, CIA 분석관, 쿠웨이트 약사, 바레인의 한국 해군 대위, 이란 대령, 테헤란 병원 지하의 노교수와 아이의 눈으로 따라간다. 등장인물과 대화는 창작이다."],
  num_h="숫자로 보는 3월 25일", num_cols=("항목", "수치", "기준"),
  nums=[("미국의 휴전안", "15개항", "파키스탄이 이란에 전달"), ("이란의 조건", "5개", "국영 매체 발표 · 15개항 거부"), ("쿠웨이트 공항 화재", "3일", "3월 25~28일 · 연료 저장소 드론 피격"),
        ("쿠웨이트가 요격한 드론", "6대", "공항 공격 당시"), ("이란 북서부 공습 사망자", "11명", "3월 25일"), ("미군 공습에 숨진 이라크군", "7명", "안바르 서부")],
  tl_h="제9화 주요 사건 타임라인 (2026.03.25)",
  tl=[("3월 25일 오전", "파키스탄, 미국의 15개항 휴전안을 이란에 전달 — 제재 완화, 핵 프로그램 후퇴, 미사일 제한, 호르무즈 재개방."),
      ("3월 25일 낮", "이란 드론, 쿠웨이트 국제공항 연료 저장소 타격 — 사흘간 화재. 요르단 암만 인근에 미사일 파편."),
      ("3월 25일 오후", "이란 국영 매체, 15개항 거부 보도 — 5개 조건 제시: 공격·암살 중단, 재발 방지, 배상, 전 전선 종전, 호르무즈 주권."),
      ("3월 25일", "테헤란 순항미사일 생산 시설 2곳 파괴. 이란 북서부 공습 11명 사망. 이란 '링컨함에 순항미사일' 주장 — 피해 없음. 이라크 안바르 미군 공습 7명 사망.")],
  vid_h="영상으로 보기 — 8개 플랫폼", vid_names=dict(longform="유튜브 롱폼 4K", shorts="유튜브 쇼츠", tiktok="틱톡", reels="인스타그램 릴스", threads="스레드", x="X", facebook="페이스북", feeds="인스타그램 피드"),
  body_h="제9화 「종이의 여행」 본문", scene="장면",
  q=["파키스탄 외교관은 15개항 문서를 어떻게 건넸나", "CIA 분석관은 왜 사직서를 저장하지 않았나", "쿠웨이트 공항이 탈 때 시민들은 무엇을 했나", "이란의 거부는 협상의 끝인가",
     "이란 대령은 왜 고개를 끄덕이지 않았나", "'싫다고 할 건데 왜 종이를 가져와요?'라는 물음에 어른은 무엇이라 답했나", "이란의 다섯 조건에서 빠진 것은 무엇인가"],
  dip="외교 분석 · Diplomatic Analysis", bg="배경 분석 · Background Analysis", chars="인물 현황 · Character Status", notes="작가 주석", nxt="다음 화 예고", src="Sources · 출처",
  dip_h="15개항과 5개 조건은 무엇이 다른가?", bg_h="이 전쟁에서 러시아는 어디에 서 있나?", fact_h="무엇이 사실이고 무엇이 창작인가", char_h="등장인물 현황 — 제9화 끝",
  faq_h="자주 묻는 질문 (FAQ)", next_h="다음 화 예고 — 제10화", src_h="출처", srcw="출처", end="— 9화 끝. 10화에서 계속됩니다. —",
  faq=[("「장대한 분노」 제9화는 어떤 내용인가요?", "2026년 3월 25일 하루, 파키스탄이 미국의 15개항 휴전안을 이란에 건네고 이란이 다섯 조건으로 답한 날을 다룹니다. 같은 날 쿠웨이트 공항이 불탔고, 인물들은 각자의 자리에서 '협상과 폭격이 같은 날 오는' 전쟁의 모순을 겪습니다."),
       ("미국의 15개항 휴전안에는 무엇이 담겼나요?", "파키스탄 관리들이 전한 바로는 이란 핵 프로그램의 후퇴, 미사일 능력의 제한, 호르무즈 해협의 재개방과 그 대가로 제재 완화가 담겼습니다. 전문은 공개되지 않았습니다."),
       ("이란의 다섯 조건은 무엇인가요?", "공격과 지도부 암살의 중단, 재발 방지 장치, 전쟁 배상, 모든 전선에서의 적대 행위 종료, 호르무즈 해협에 대한 이란의 주권 행사입니다."),
       ("쿠웨이트 공항에서는 무슨 일이 있었나요?", "3월 25일 이란 드론이 쿠웨이트 국제공항의 연료 저장소를 맞혀 불이 났고, 사흘 동안 타다가 3월 28일에 꺼졌습니다. 쿠웨이트는 다른 드론 여섯 대를 요격했다고 밝혔습니다."),
       ("이 소설은 실화인가요?", "아닙니다. 공개 보도로 확인되는 사실을 뼈대로 삼은 픽션입니다. 타리크 메흐무드, 레일라 시라지 같은 인물과 모든 대화, 기밀 문서는 창작입니다."),
       ("영상으로도 볼 수 있나요?", "네. 유튜브 롱폼(4K, 8분 30초 이상), 쇼츠·틱톡·릴스(2분 30초~3분), 스레드, X, 페이스북, 인스타그램 피드 영상으로 제작되었고, 한국어·영어·일본어 내레이션과 자막이 있습니다.")],
  disc="이 소설은 2026년 2월 28일 개시된 미국·이스라엘의 대이란 군사작전(Operation Epic Fury)과 그 이후의 전쟁에서 착상을 얻은 픽션입니다. 등장인물, 대화, 내면, 기밀 문서는 모두 창작이며, 실존 인물에게 부여된 발언과 판단 역시 지어낸 것입니다. 사실 보도나 정세 분석용이 아닙니다.",
  tags=["장대한분노", "에픽퓨리", "EpicFury", "호르무즈의밤", "전쟁소설", "이란전쟁", "15개항", "휴전안", "쿠웨이트공항", "연재소설"],
  kw=["장대한 분노", "에픽 퓨리", "Epic Fury", "이란 전쟁 소설", "15개항 휴전안", "이란 다섯 조건", "쿠웨이트 공항 화재", "파키스탄 중재", "호르무즈 해협"]),
 "en": dict(
  title="Epic Fury Episode 9, “The Journey of a Paper” — The U.S. 15-Point Ceasefire Plan and Iran’s Five Conditions (A Novel of the 2026 Iran War)",
  desc="On March 25, 2026, Pakistan delivered a fifteen-point U.S. ceasefire plan to Iran. Iran said no and laid out five conditions. The same day, Kuwait’s airport burned. Episode 9 of the war novel Epic Fury: summary, timeline, the two papers compared, and what is fact and what is fiction.",
  meta="Serialized novel “Epic Fury: Night Over Hormuz” · Episode 9 · Story date March 25, 2026 (War Day 26)",
  tldr_h="At a Glance — Episode 9 in Brief",
  tldr=["On March 25, Pakistan delivered a fifteen-point U.S. ceasefire plan to Iran: sanctions relief in exchange for rolling back the nuclear program, limiting missiles, and reopening the Strait of Hormuz.",
        "The same day, Iranian state media reported a rejection and five conditions: an end to attacks and assassinations, guarantees against another war, reparations, an end to fighting on all fronts, and sovereignty over the Strait of Hormuz.",
        "That day an Iranian drone hit the fuel depot at Kuwait International Airport; the fire burned for three days. Talks and bombs arrived on the same day.",
        "The novel follows that day through a Pakistani diplomat, a CIA analyst, a Kuwaiti pharmacist, a South Korean naval officer in Bahrain, an Iranian colonel, and an old professor and a child in a Tehran hospital basement. Characters and dialogue are fiction."],
  num_h="March 25 in Numbers", num_cols=("Item", "Figure", "Note"),
  nums=[("U.S. ceasefire plan", "15 points", "Delivered by Pakistan"), ("Iran's conditions", "5", "State media · rejection of the 15 points"), ("Kuwait airport fire", "3 days", "Mar 25–28 · fuel depot hit by drone"),
        ("Drones Kuwait intercepted", "6", "During the airport attack"), ("Killed in NW Iran strikes", "11", "March 25"), ("Iraqi soldiers killed by U.S. strike", "7", "Western Anbar")],
  tl_h="Episode 9 Timeline (March 25, 2026)",
  tl=[("Mar 25, morning", "Pakistan delivers the U.S. fifteen-point ceasefire plan to Iran — sanctions relief, nuclear rollback, missile limits, reopening Hormuz."),
      ("Mar 25, midday", "Iranian drone hits Kuwait International Airport's fuel depot — fire for three days. Missile debris near Amman, Jordan."),
      ("Mar 25, afternoon", "Iranian state media reports rejection — five conditions: end attacks and assassinations, no recurrence, reparations, end war on all fronts, Hormuz sovereignty."),
      ("Mar 25", "Two cruise missile production sites in Tehran destroyed. Eleven killed in NW Iran. Iran claims a cruise missile attack on USS Abraham Lincoln — no damage. Seven Iraqi soldiers killed in Anbar.")],
  vid_h="Watch — Eight Platforms", vid_names=dict(longform="YouTube long form 4K", shorts="YouTube Shorts", tiktok="TikTok", reels="Instagram Reels", threads="Threads", x="X", facebook="Facebook", feeds="Instagram Feed"),
  body_h="Episode 9, “The Journey of a Paper”", scene="Scene",
  q=["How did a Pakistani diplomat hand over the fifteen points?", "Why didn't the CIA analyst save her resignation letter?", "What did people in Kuwait do as the airport burned?", "Is Iran's rejection the end of talks?",
     "Why did the Iranian colonel not nod?", "\"Why bring the paper if we say no?\" — what did the grown-up answer?", "What was missing from Iran's five conditions?"],
  dip="Diplomatic Analysis · Diplomatic Analysis", bg="Background Analysis", chars="Character Status", notes="Author’s Note", nxt="Next Episode", src="Sources",
  dip_h="How do the fifteen points and the five conditions differ?", bg_h="Where does Russia stand in this war?", fact_h="What Is Fact and What Is Fiction", char_h="Characters at the End of Episode 9",
  faq_h="Frequently Asked Questions", next_h="Next — Episode 10", src_h="Sources", srcw="Source", end="— End of Episode 9. Continued in Episode 10. —",
  faq=[("What is Epic Fury Episode 9 about?", "It covers March 25, 2026, the day Pakistan handed Iran a fifteen-point U.S. ceasefire plan and Iran answered with five conditions. The same day Kuwait's airport burned, and the characters live through a war in which talks and bombs arrive together."),
       ("What was in the U.S. fifteen-point plan?", "According to Pakistani officials: rolling back Iran's nuclear program, limits on missile capabilities, and reopening the Strait of Hormuz, in exchange for sanctions relief. The full text was not published."),
       ("What are Iran's five conditions?", "An end to attacks and to the assassination of its leaders, a mechanism to prevent another war, reparations, an end to hostilities on all fronts, and Iranian sovereignty over the Strait of Hormuz."),
       ("What happened at Kuwait's airport?", "On March 25 an Iranian drone hit the fuel depot at Kuwait International Airport. The fire burned for three days until March 28. Kuwait said it intercepted six other drones."),
       ("Is this a true story?", "No. It is fiction built on facts confirmed by public reporting. Characters such as Tariq Mehmood and Leila Shirazi, all dialogue, and the classified documents are invented."),
       ("Is there a video version?", "Yes: a YouTube long form (4K, over 8:30), Shorts/TikTok/Reels (2:30–3:00), and Threads, X, Facebook and Instagram Feed videos, narrated and subtitled in Korean, English and Japanese.")],
  disc="This novel is a work of fiction inspired by the U.S.–Israeli military operation against Iran (Operation Epic Fury) launched on February 28, 2026, and the war that followed. Characters, dialogue, inner thoughts and classified documents are invented, as are the statements attributed to real people. It is not intended as factual reporting or analysis.",
  tags=["EpicFury", "NightOverHormuz", "WarNovel", "IranWar", "Ceasefire", "StraitOfHormuz", "Kuwait", "Pakistan", "SerialFiction"],
  kw=["Epic Fury", "Night Over Hormuz", "Iran war novel", "15-point ceasefire plan", "Iran five conditions", "Kuwait airport fire", "Pakistan mediation", "Strait of Hormuz"]),
}
SCENE_PAGE = [6, 9, 12, 15, 18, 21, 24]  # first page of each scene → its video still

def lines(L): return open(f"{D}/ep09_{L}.txt").read().splitlines()
def section(L, start, n):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == start)
    return ls[i + 1:i + 1 + n]
def notes(L, t):
    ls = lines(L); i = next(k for k, x in enumerate(ls) if x.strip() == t["notes"]); j = next(k for k, x in enumerate(ls) if x.strip() == t["nxt"])
    blk = ls[i + 1:j]; return [(blk[k], blk[k + 1]) for k in range(0, len(blk) - 1, 2)]
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
def img_key(n): return f"vid9_p{n:02d}"
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
    H.append(fig("vid9_c_longform", t["tldr"][0][:60] + "…"))
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
    H.append(fig("vid9_p03", t["tl"][1][1]))
    H.append(h("h2", E(t["vid_h"])))
    V = VID.format(L=L)
    if mode in ("wordpress", "tistory"): H.append(fig("vid9_c_longform", t["vid_names"]["longform"], video=V + f"epic_fury_ep09_longform_{L}.mp4"))
    links = [(t["vid_names"][k], V + f"epic_fury_ep09_{k}_{L}.mp4") for k in PLATS]
    H.append("<ul>" + "".join(f'<li><a href="{u}">{E(n)}</a></li>' for n, u in links) + "</ul>")
    H.append(h("h2", E(t["body_h"])))
    for i, sc in enumerate(SC):
        paras = sc["paras"]
        if i == 6: paras = paras[:12]
        H.append(h("h2", f"{t['scene']} {i + 1}. {E(t['q'][i])}"))
        intro = f'<p{st("font-weight:800;color:#0b2245;margin:0 0 4px")} class="place"><b>{E(sc["place"])}</b></p><p{st("font-size:15px;color:#555;margin:0 0 14px")} class="time"><i>{E(sc["time"])}</i></p>'
        cls = lambda c: {"dialogue": "dlg", "factual": "fact", "impact": "impact", "shareable": "impact"}.get(c, "")
        body = "".join((f"<blockquote>{E(x)}</blockquote>" if mode == "substack" and c in ("impact", "shareable") else p(x, cls(c))) for c, x in paras)
        f = fig(img_key(SCENE_PAGE[i]), sc["place"])
        if mode in ("wordpress", "tistory"):
            first = "".join(p(x, cls(c)) for c, x in paras[:2]); rest = "".join(p(x, cls(c)) for c, x in paras[2:])
            H.append(f'<div class="row"><div class="col">{intro}{first}</div>{f}</div>{rest}')
        else: H.append(intro + f + body)
    H.append(p(t["end"]))
    d = section(L, t["dip"], 4)
    H.append(h("h2", E(t["dip_h"])) + "".join(p(x) for x in d[1:]))
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
    for k in ["vid9_c_longform", "vid9_p03"] + [img_key(n) for n in SCENE_PAGE]:
        if k in seen: continue
        seen.append(k); m = MAN[k]; items.append((f"{m['title']} — {credit(k, t)}", m["page"]))
    H.append("<ol>" + "".join(f'<li>{E(a)}<br><a href="{E(u)}">{E(u)}</a></li>' for a, u in items) + "</ol>")
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
         "keywords": ", ".join(t["kw"]), "image": [img_url("vid9_c_longform")], "author": {"@type": "Organization", "name": "Epic Fury · SOULTHREAD"},
         "isPartOf": {"@type": "CreativeWorkSeries", "name": "Epic Fury: Night Over Hormuz"},
         "about": [{"@type": "Thing", "name": "2026 Iran war"}, {"@type": "Place", "name": "Islamabad"}, {"@type": "Place", "name": "Kuwait International Airport"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]]},
        {"@type": "VideoObject", "name": t["vid_names"]["longform"] + " — " + t["title"][:60], "description": t["desc"], "thumbnailUrl": img_url("vid9_c_longform"),
         "uploadDate": POSTED, "contentUrl": V + f"epic_fury_ep09_longform_{L}.mp4", "inLanguage": L}]}
    return (f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={fq}:wght@400;500;700;800;900&display=swap"><style>{css}</style>\n'
            f'<div class="efb">\n{body}\n</div>\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

def page(L, mode, b):
    t = T[L]; fq = "Noto+Sans+KR" if L == "ko" else "Noto+Sans"
    extra = "" if mode in ("wordpress", "tistory") else f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family={fq}:wght@400;700;900&display=swap'><style>body{{font-family:'Noto Sans KR','Noto Sans',sans-serif;font-size:19px;line-height:1.9;max-width:860px;margin:0 auto;padding:16px}} img{{max-width:100%;height:auto}}</style>"
    return (f"<!doctype html><html lang='{L}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{E(t['title'])}</title>"
            f"<meta name='description' content='{E(t['desc'])}'><meta name='keywords' content='{E(', '.join(t['kw']))}'><meta property='og:title' content='{E(t['title'])}'>"
            f"<meta property='og:description' content='{E(t['desc'])}'><meta property='og:image' content='{img_url('vid9_c_longform')}'><meta property='og:type' content='article'>{extra}</head>"
            f"<body style='background:#fbf9f4;margin:0;padding:16px'>{b}</body></html>")

if __name__ == "__main__":
    for L, mode in [("ko", "naver"), ("ko", "tistory"), ("ko", "wordpress"), ("ko", "substack"), ("en", "wordpress"), ("en", "substack")]:
        b = build(L, mode); base = f"{OUT}/epic_fury_ep09_blog_{mode}_{L}"
        open(base + ".html", "w").write(page(L, mode, b)); open(base + "_body.html", "w").write(b); print(L, mode, len(b))
