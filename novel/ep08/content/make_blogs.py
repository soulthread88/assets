# -*- coding: utf-8 -*-
"""EP08 블로그 4종(WordPress, Tistory, Naver, Substack) 생성 — GEO(생성형 엔진 최적화) 구조.
요약 → 핵심 숫자 → 타임라인 → 영상 → 장면 8개(이미지 박스 + 출처) → 배경 지식 → 사실/창작 구분 → FAQ → 출처."""
import json, html, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content_ep08_ko as K
E = html.escape
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/blog"; os.makedirs(OUT, exist_ok=True)
MAN = json.load(open("/home/claude/work/media_ep08/manifest.json"))
SC = json.load(open(f"{D}/scenes_full.json"))
IMG = "https://raw.githubusercontent.com/soulthread88/imgs/main/novel/ep08/"
VID = "https://media.githubusercontent.com/media/soulthread88/videos/main/novel/ep08/platform_ko/"
POSTED = "2026-11-11"

TITLE = "장대한 분노 제8화 「핵의 문턱」 — 나탄즈와 디모나, 서로의 핵시설을 겨눈 날 (2026 이란 전쟁 소설)"
DESC = ("2026년 3월 21~24일, 미국의 벙커버스터가 이란 나탄즈 핵시설을, 이란의 미사일이 이스라엘 디모나를 때렸다. "
        "48시간 발전소 최후통첩과 닷새 연기까지 — 실제 사건에서 착상한 전쟁 소설 「장대한 분노」 제8화 줄거리, 타임라인, 사실과 창작의 구분.")
KEYWORDS = ["장대한 분노", "에픽 퓨리", "Epic Fury", "호르무즈의 밤", "이란 전쟁 소설", "나탄즈", "디모나", "아라드", "발전소 최후통첩", "포르도", "2026 이란 전쟁"]
TLDR = ["3월 21일 미국이 벙커버스터로 이란 나탄즈 핵시설을 타격했고, 같은 날 저녁 이란 미사일이 이스라엘 디모나에 떨어져 건물이 무너졌다(부상 64~78명 이상, 인근 아라드 116명).",
        "두 나라가 같은 날 서로의 핵 관련 시설을 겨눈 것은 이번이 처음이다. 국제원자력기구(IAEA)는 핵 사고 위험을 경고하며 자제를 촉구했다.",
        "트럼프 대통령은 48시간 안에 호르무즈 해협을 열지 않으면 이란 발전소를 치겠다고 했다가, 3월 23일 '생산적 협상'을 이유로 닷새 미뤘다. 이란은 협상을 부인했다.",
        "소설은 이 나흘을 CIA 분석관, 항공모함 함장, 이란 방공군 대령, 테헤란의 간호사와 철학 교수의 눈으로 따라간다. 등장인물과 대화는 창작이다."]
NUMBERS = [("디모나 부상자", "64~78명 이상", "3월 21일 · 건물 붕괴"), ("아라드 부상자", "116명", "3월 21일 · 7명 중상"),
           ("최후통첩 시한", "48시간", "3월 21일 · 해협 미개방 시 발전소 타격"), ("연기된 날수", "5일", "3월 23일 · '생산적 협상' 이유, 이란은 부인"),
           ("하루 공습 기록", "379건", "3월 23일 · 20개 주, 대부분 테헤란"), ("하루 민간인 사망", "38명", "3월 23일 · HRANA 집계")]
TIMELINE = [("3월 21일(토) · 전쟁 22일째", "미국, 벙커버스터로 나탄즈 핵시설 타격 — IAEA 자제 촉구. 이스라엘, 테헤란 말렉 아슈타르 공대 타격. 저녁, 이란 미사일이 디모나와 아라드에 떨어져 180명 가까이 부상. 트럼프, 48시간 최후통첩."),
            ("3월 22일(일) · 전쟁 23일째", "반다르 아바스 발전소 두 곳 피격. 이스라엘 중부에서 미사일로 15명 부상. 헤즈볼라 로켓으로 미스가브 암에서 1명 사망."),
            ("3월 23일(월) · 전쟁 24일째", "트럼프, 발전소 타격 닷새 연기 — '생산적 협상'. 이란 '협상 없다'. 테헤란 중심으로 379건 공습, 민간인 38명 사망. 전국에 바시즈 순찰대와 검문소."),
            ("3월 24일(화) · 전쟁 25일째", "이란, 졸가드르를 국가안보최고회의 서기에 임명. 이란 미사일이 텔아비브·에일라트·디모나·하이파로. 바레인 드론 공격으로 노동자 사망. 이라크 안바르 미군 공습으로 인민동원군 15명 사망.")]
SCENE_IMG = ["img_ep8_natanz", "ai_ep8_analyst", "img_ep8_telaviv40", "img_ep8_ford_souda5", "ai_ep8_command", "ai_ep8_candle", "img_ep8_radio", "img_ep8_souda_welcome"]
SCENE_ALT = ["이란 이스파한 주 나탄즈 일대의 산과 길 — 우라늄 농축 단지가 있는 지역",
             "밝은 사무실에서 파형 그래프를 보는 분석관 (AI 생성 일러스트)",
             "이란 미사일이 떨어진 직후의 텔아비브 주택가, 2026년 3월 24일",
             "크레타 섬 수다 만에 정박한 미 항공모함 제럴드 R. 포드함과 해군 장병들",
             "눈 덮인 산맥을 내다보는 방공 지휘소의 장교 (AI 생성 일러스트)",
             "병원 계단에서 반쯤 탄 양초를 쥔 간호사의 손 (AI 생성 일러스트)",
             "단파 라디오 수신기 — 외국 방송과 국영 방송이 서로 다른 말을 하던 밤",
             "크레타 섬 수다 만 — 미 해군 지원시설 앞바다"]
SCENE_Q = ["나탄즈 핵시설이 맞았을 때 지하에서는 무슨 일이 있었나",
           "포르도의 신호는 왜 5.7초에서 5.2초로 빨라졌나",
           "디모나 주민들은 왜 자기 도시가 안전하다고 믿었나",
           "발전소는 전쟁에서 적법한 표적인가",
           "이란 방공군 대령은 디모나를 향한 탄도를 보며 무엇을 느꼈나",
           "발전소가 꺼지면 병원은 며칠을 버틸 수 있나",
           "'협상이 있다'와 '협상은 없다' 사이에서 철학 교수는 무엇을 읽었나",
           "함장은 왜 '아직은'이라고 말했나"]
HISTORY = [("나탄즈는 어떤 곳인가?", "나탄즈는 이스파한 주에 있는 이란 최대의 우라늄 농축 단지다. 주 농축 시설은 흙과 콘크리트 아래에 묻혀 있다. 2010년 스턱스넷 악성 코드, 2020년과 2021년의 파괴 공작, 2025년 6월의 폭격을 차례로 겪었고, 이번 전쟁에서는 3월 2일과 3월 21일에 맞았다. 미국이 쓴 벙커버스터 GBU-57은 무게 약 13,600킬로그램으로, 2025년 6월 포르도와 나탄즈에 처음 실전 투하되었다."),
           ("디모나는 어떤 곳인가?", "디모나는 이스라엘 남부 네게브 사막의 도시다. 인근에 1950년대 말 프랑스의 지원으로 지은 시몬 페레스 네게브 핵연구센터가 있다. 이스라엘은 핵무기 보유를 인정하지도 부인하지도 않는 모호성 정책을 지켜 왔다. 3월 21일 이란의 미사일이 이 도시의 주거 지역에 떨어졌다."),
           ("핵시설 공격에는 선례가 있나?", "운영 중인 핵시설에 대한 군사 공격은 1981년 이스라엘의 이라크 오시라크 원자로 폭격, 2007년 시리아 알키바르 폭격 같은 선례가 있다. 그러나 두 나라가 같은 날 서로의 핵 관련 시설을 겨눈 것은 이날이 처음이었다."),
           ("발전소 공격은 전쟁법상 허용되나?", "전력 시설은 군사 목적에 실질적으로 기여할 때에 한해 표적이 될 수 있고, 그때에도 예상되는 민간 피해가 군사적 이익에 비해 과도하면 공격이 금지된다(구별과 비례의 원칙). 한 나라의 발전소 전체를 겨누는 것이 이 기준에 맞는지는 이 전쟁 내내 논쟁거리였다.")]
FACT = [("나탄즈 타격 (3월 21일)", "실존 사건", "미국이 벙커버스터로 나탄즈 핵시설을 타격했다. IAEA는 자제를 촉구했다. 작중의 현장 묘사는 창작이다."),
        ("디모나·아라드 (3월 21일)", "실존 사건", "디모나에서 건물이 무너져 64~78명 이상, 아라드에서 116명이 다쳤다. 갈리트 아미르는 가상 인물이다."),
        ("발전소 최후통첩 (3월 21~23일)", "실존 사건", "48시간 최후통첩 뒤 3월 23일 닷새 연기. 이란은 협상을 부인했다."),
        ("포르도의 5.2초", "작중 설정", "포르도 신호와 그 변화는 소설의 창작이다. 포르도 가동에 관한 공개 정보는 없다."),
        ("모하마드 바게르 졸가드르", "실존 인물", "혁명수비대 출신 강경파. 3월 24일 국가안보최고회의 서기에 임명되었다."),
        ("포드함과 수다 만", "실존 경과 · 작중 설정", "포드함은 화재 뒤 수다 만에서 수리를 받았다. 함장과 기자의 통화, '서른 초'는 창작이다.")]
CHARS = [("레일라 시라지", "CIA 이란 작전센터 분석관", "포르도의 가속을 포착하고, 파키스탄을 통한 접촉을 권고하는 문장을 지우지 않았다."),
         ("마커스 웹", "미 항공모함 포드함 함장", "발전소가 적법한 표적인지 물었고, 스물다섯 해 만에 처음으로 기자에게 자기 생각을 말했다."),
         ("새라 캘러한", "AP 종군기자", "수첩을 덮고, 기자로서가 아닌 전화를 걸었다."),
         ("다리우스 세파흐반드", "이란 방공군 대령", "디모나를 향한 탄도를 보았고, 서른한 해 버틴 들보에 금이 가는 소리를 들었다."),
         ("마리암", "이맘 호메이니 병원 간호사", "비상 발전기 연료를 세었다. 전체 서른 시간, 중환자실만 나흘."),
         ("아자드 모라디", "테헤란대 철학 교수", "대화가 있다는 말과 없다는 말 사이에서 탁자를 읽고, 아래층 문 앞에 초 여섯 자루를 놓았다.")]
FAQ = [("「장대한 분노」 제8화는 어떤 내용인가요?", "2026년 3월 21~24일, 미국과 이란이 같은 날 서로의 핵 관련 시설(나탄즈, 디모나)을 겨눈 나흘을 다룹니다. 발전소 최후통첩과 닷새 연기를 사이에 두고, 분석관·함장·대령·간호사·철학 교수가 각자의 자리에서 전쟁의 문턱을 지켜봅니다."),
       ("이 소설은 실화인가요?", "아닙니다. 2026년 이란 전쟁의 공개 보도로 확인되는 사실(날짜, 공습, 피해 집계)을 뼈대로 삼은 픽션입니다. 등장인물, 대화, 기밀 문서, 포르도 신호 같은 설정은 모두 창작입니다."),
       ("3월 21일 나탄즈에서는 무엇이 일어났나요?", "미국이 벙커버스터 폭탄으로 나탄즈 핵시설을 타격했습니다. 이란은 우라늄 농축 센터가 공습을 받았다고 밝혔고, 국제원자력기구는 핵 사고 위험을 피하도록 자제를 촉구했습니다."),
       ("디모나와 아라드의 피해 규모는?", "3월 21일 저녁 디모나에서 건물 한 채가 무너져 집계에 따라 64~78명 이상이 다쳤고, 인근 아라드에서 116명이 다쳐 7명이 중상을 입었습니다."),
       ("발전소 최후통첩은 어떻게 되었나요?", "트럼프 대통령은 3월 21일 48시간 최후통첩을 보냈고, 3월 23일 '생산적인 협상'을 이유로 발전소 타격을 닷새 미뤘습니다. 이란 외무부는 협상은 없다고 부인했습니다."),
       ("영상과 오디오로도 볼 수 있나요?", "네. 유튜브 롱폼(4K, 약 8분), 쇼츠(약 2분), 인스타그램 피드 영상으로 제작되었고, 한국어 AI 내레이션과 자막이 들어 있습니다.")]
SOURCES = [("Wikipedia — Timeline of the 2026 Iran war", "https://en.wikipedia.org/wiki/Timeline_of_the_2026_Iran_war"),
           ("Wikipedia — 2026 Iran war", "https://en.wikipedia.org/wiki/2026_Iran_war"),
           ("Wikipedia — USS Gerald R. Ford", "https://en.wikipedia.org/wiki/USS_Gerald_R._Ford"),
           ("Wikipedia — Fordow Fuel Enrichment Plant", "https://en.wikipedia.org/wiki/Fordow_Fuel_Enrichment_Plant"),
           ("Wikipedia — Natanz Nuclear Facility", "https://en.wikipedia.org/wiki/Natanz_Nuclear_Facility"),
           ("Wikipedia — Shimon Peres Negev Nuclear Research Center", "https://en.wikipedia.org/wiki/Shimon_Peres_Negev_Nuclear_Research_Center")]
NEXT = "3월 25일. 닷새의 말미. 시한이 다시 다가온다. 워싱턴은 이란이 협상을 구걸한다고 말하고, 테헤란은 협상이 없다고 말한다. 그 사이에서 종이 한 장이 나라에서 나라로 건너간다. 그리고 이슬라마바드의 그 방에, 이번에는 정말로 사람들이 앉는다."
DISCLAIMER = "이 소설은 2026년 2월 28일 개시된 미국·이스라엘의 대이란 군사작전(Operation Epic Fury)과 그 이후의 전쟁에서 착상을 얻은 픽션입니다. 등장인물, 대화, 내면, 기밀 문서는 모두 창작이며, 실존 인물에게 부여된 발언과 판단 역시 지어낸 것입니다. 사실 보도나 정세 분석용이 아닙니다."
HASHTAGS = ["장대한분노", "에픽퓨리", "EpicFury", "호르무즈의밤", "전쟁소설", "이란전쟁", "나탄즈", "디모나", "웹소설", "연재소설"]

def img_url(k): return IMG + MAN[k]["file"]
def credit_txt(k):
    m = MAN[k]
    if m["site"].startswith("AI"): return "AI 생성 이미지 · GPT Image 2 (Magica)"
    return " · ".join(x for x in [m.get("author"), m.get("license"), m.get("site")] if x)
def scene_title(i):
    tag, h2 = K.SCENES[i][0], K.SCENES[i][1]
    return h2, tag

# ---------------- styles ----------------
C = dict(ink="#141414", navy="#0b2245", red="#c8202d", gold="#f2b21b", sub="#555", line="#e3dccb", bg="#fbf9f4", box="#f3eee2")
ST = {  # inline styles (Naver / fallback)
 "wrap": f"font-family:'Noto Sans KR','Malgun Gothic',sans-serif;color:{C['ink']};font-size:19px;line-height:1.9;word-break:keep-all;max-width:860px;margin:0 auto",
 "h1": f"font-size:32px;line-height:1.35;font-weight:900;color:{C['navy']};margin:0 0 12px",
 "h2": f"font-size:26px;line-height:1.4;font-weight:800;color:{C['navy']};margin:44px 0 14px;padding-left:14px;border-left:8px solid {C['gold']}",
 "h3": f"font-size:21px;font-weight:800;color:{C['red']};margin:24px 0 8px",
 "p": "margin:0 0 18px",
 "meta": f"font-size:16px;color:{C['sub']};margin:0 0 20px",
 "tldr": f"background:{C['box']};border:2px solid {C['gold']};border-radius:10px;padding:18px 24px;margin:18px 0 28px",
 "fig": "margin:22px 0 26px",
 "img": "display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:8px",
 "cap": f"font-size:16px;color:{C['ink']};margin:8px 0 2px;font-weight:500",
 "src": f"font-size:14px;font-style:italic;color:{C['sub']};margin:0",
 "table": "width:100%;border-collapse:collapse;margin:10px 0 24px;font-size:17px",
 "th": f"background:{C['navy']};color:#fff;padding:10px;text-align:left;border:1px solid {C['navy']}",
 "td": f"padding:10px;border:1px solid {C['line']};vertical-align:top",
 "num": f"font-size:22px;font-weight:900;color:{C['red']}",
 "quote": f"margin:18px 0;padding:14px 20px;background:#fff;border-left:6px solid {C['red']};font-weight:700;color:{C['navy']}",
 "disc": f"font-size:15px;color:{C['sub']};background:{C['box']};padding:14px 18px;border-radius:8px;margin:24px 0",
 "btn": f"display:inline-block;background:{C['red']};color:#fff;font-weight:800;padding:10px 18px;border-radius:8px;text-decoration:none;margin:4px 8px 4px 0",
}
CSS = f"""
.efb{{{ST['wrap']}}}
.efb h1{{{ST['h1']}}} .efb h2{{{ST['h2']}}} .efb h3{{{ST['h3']}}} .efb p{{{ST['p']}}}
.efb .meta{{{ST['meta']}}} .efb .tldr{{{ST['tldr']}}} .efb .tldr ul{{margin:8px 0 0;padding-left:22px}}
.efb figure{{{ST['fig']}}} .efb figure img,.efb figure video{{{ST['img']}}}
.efb figcaption .cap{{{ST['cap']}}} .efb figcaption .src{{{ST['src']}}} .efb figcaption .src a{{color:{C['sub']}}}
.efb table{{{ST['table']}}} .efb th{{{ST['th']}}} .efb td{{{ST['td']}}} .efb .num{{{ST['num']}}}
.efb blockquote{{{ST['quote']}}} .efb .disc{{{ST['disc']}}} .efb .btn{{{ST['btn']}}}
.efb .row{{display:flex;gap:28px;align-items:center;flex-wrap:wrap;margin:18px 0 8px}}
.efb .row .col{{flex:1 1 380px;min-width:0}} .efb .row figure{{flex:1 1 380px;margin:0}}
.efb .place{{font-weight:800;color:{C['navy']};font-size:17px;margin:0 0 4px}} .efb .time{{font-size:15px;color:{C['sub']};margin:0 0 14px}}
.efb .dlg{{padding-left:14px;border-left:3px solid {C['line']}}} .efb .fact{{background:{C['box']};padding:12px 16px;border-radius:8px;font-size:17px}}
.efb .impact{{font-weight:800;color:{C['red']}}}
.efb .faq dt{{font-weight:800;color:{C['navy']};margin-top:16px}} .efb .faq dd{{margin:6px 0 0 0}}
.efb .tags{{color:{C['sub']};font-size:16px}}
@media (max-width:640px){{.efb{{font-size:18px}} .efb h1{{font-size:26px}} .efb h2{{font-size:22px}}}}
"""

def figure(k, alt, cap, mode, video=None):
    m = MAN.get(k, {})
    link = m.get("page", "")
    if mode == "substack":
        media = f'<img src="{img_url(k)}" alt="{E(alt)}">'
        return f'<figure>{media}<figcaption>{E(cap)} — 출처: <a href="{E(link)}">{E(credit_txt(k))}</a></figcaption></figure>'
    if mode == "naver":
        return (f'<p style="margin:22px 0 4px"><img src="{img_url(k)}" alt="{E(alt)}" style="width:100%;height:auto"></p>'
                f'<p style="{ST["cap"]}">{E(cap)}</p><p style="{ST["src"]}"><i>출처: <a href="{E(link)}" style="color:#555">{E(credit_txt(k))}</a></i></p>')
    media = (f'<video controls preload="metadata" poster="{img_url(k)}" src="{video}"></video>' if video else
             f'<img src="{img_url(k)}" alt="{E(alt)}" width="3840" height="2160" loading="lazy">')
    return (f'<figure>{media}<figcaption><p class="cap">{E(cap)}</p>'
            f'<p class="src"><i>출처: <a href="{E(link)}" target="_blank" rel="noopener">{E(credit_txt(k))}</a></i></p></figcaption></figure>')

def para(c, t, mode):
    cls = {"dialogue": "dlg", "factual": "fact", "impact": "impact", "shareable": "impact"}.get(c, "")
    if mode == "substack":
        if c in ("impact", "shareable"): return f"<blockquote>{E(t)}</blockquote>"
        return f"<p>{E(t)}</p>"
    if mode == "naver":
        sty = {"dlg": "padding-left:14px;border-left:3px solid #e3dccb", "fact": f"background:{C['box']};padding:12px 16px;font-size:17px",
               "impact": f"font-weight:800;color:{C['red']}"}.get(cls, "")
        return f'<p style="{ST["p"]};{sty}">{E(t)}</p>'
    return f'<p class="{cls}">{E(t)}</p>' if cls else f"<p>{E(t)}</p>"

def build(mode):
    n = lambda tag, inner, key=None: (f'<{tag} style="{ST[key or tag]}">{inner}</{tag}>' if mode == "naver" else f"<{tag}>{inner}</{tag}>")
    H = []
    H.append(n("h1", E(TITLE)))
    H.append(f'<p class="meta" style="{ST["meta"]}">연재 소설 「장대한 분노: 호르무즈의 밤」 · 제8화 · 작중 시점 2026년 3월 21~24일(전쟁 22~25일째) · 게시 {POSTED}</p>'
             if mode != "substack" else f"<p><em>연재 소설 「장대한 분노: 호르무즈의 밤」 · 제8화 · 작중 시점 2026년 3월 21~24일 · 게시 {POSTED}</em></p>")
    H.append(figure("img_ep8_b52_42", "이륙하는 B-52 폭격기, 2026년 3월 22일", "'장대한 분노' 작전 중 이륙하는 미 공군 B-52 폭격기, 2026년 3월 22일. 전날 미국은 이란 발전소를 치겠다는 48시간 최후통첩을 보냈다.", mode))
    # TL;DR
    li = "".join(f"<li>{E(x)}</li>" for x in TLDR)
    if mode == "naver":
        H.append(f'<div style="{ST["tldr"]}"><p style="margin:0;font-weight:900;color:{C["navy"]}">한눈에 보기 — 제8화 핵심 요약</p><ul style="margin:8px 0 0;padding-left:22px">{li}</ul></div>')
    elif mode == "substack":
        H.append(f"<h2>한눈에 보기 — 제8화 핵심 요약</h2><ul>{li}</ul>")
    else:
        H.append(f'<div class="tldr"><strong>한눈에 보기 — 제8화 핵심 요약</strong><ul>{li}</ul></div>')
    # numbers
    H.append(n("h2", "숫자로 보는 3월 21~24일"))
    rows = "".join((f'<tr><td style="{ST["td"]}">{E(a)}</td><td style="{ST["td"]}"><span style="{ST["num"]}">{E(b)}</span></td><td style="{ST["td"]}">{E(c)}</td></tr>' if mode == "naver"
                    else f'<tr><td>{E(a)}</td><td><span class="num">{E(b)}</span></td><td>{E(c)}</td></tr>') for a, b, c in NUMBERS)
    if mode == "substack":
        H.append("<ul>" + "".join(f"<li><strong>{E(a)}: {E(b)}</strong> — {E(c)}</li>" for a, b, c in NUMBERS) + "</ul>")
    else:
        th = (lambda x: f'<th style="{ST["th"]}">{x}</th>') if mode == "naver" else (lambda x: f"<th>{x}</th>")
        H.append(f'<table style="{ST["table"]}">' if mode == "naver" else "<table>")
        H[-1] += f"<thead><tr>{th('항목')}{th('수치')}{th('기준')}</tr></thead><tbody>{rows}</tbody></table>"
    # timeline
    H.append(n("h2", "제8화 주요 사건 타임라인 (2026.03.21~24)"))
    for d, t in TIMELINE:
        H.append(n("h3", E(d)) + para("", t, mode))
    H.append(figure("img_ep8_telaviv39", "이란 미사일 낙하 직후 텔아비브 주택가의 구조대", "이란 미사일이 떨어진 직후의 텔아비브 주택가, 2026년 3월 24일. 3월 21일에는 디모나와 아라드에서 180명 가까이 다쳤다.", mode))
    # video
    H.append(n("h2", "영상으로 보기 — 4K 롱폼 · 쇼츠 · 인스타그램 피드"))
    vids = [("유튜브 롱폼 (3840×2160)", "epic_fury_ep08_longform_ko.mp4"), ("쇼츠 (2160×3840)", "epic_fury_ep08_shorts_ko.mp4"), ("인스타그램 피드 (2160×2700)", "epic_fury_ep08_feeds_ko.mp4")]
    if mode in ("wordpress", "tistory"):
        H.append(figure("img_ep8_b52_42", "제8화 롱폼 영상", "장대한 분노 제8화 「핵의 문턱」 4K 롱폼 영상 — 한국어 AI 내레이션·자막 포함", mode, video=VID + vids[0][1]))
    links = "".join((f'<a href="{VID}{f}" style="{ST["btn"]}">{E(l)}</a>' if mode == "naver" else
                     (f'<li><a href="{VID}{f}">{E(l)}</a></li>' if mode == "substack" else f'<a class="btn" href="{VID}{f}" target="_blank" rel="noopener">{E(l)}</a>')) for l, f in vids)
    H.append(f"<ul>{links}</ul>" if mode == "substack" else f"<p>{links}</p>")
    # scenes
    H.append(n("h2", "제8화 「핵의 문턱」 본문"))
    for i, sc in enumerate(SC):
        h2, tag = scene_title(i)
        paras = sc["paras"][:17] if i == 7 else sc["paras"]
        H.append(n("h2", f"장면 {i+1}. {E(h2)} — {E(SCENE_Q[i])}"))
        intro = (f'<p class="place" style="font-weight:800;color:{C["navy"]};margin:0 0 4px">{E(sc["place"])}</p><p class="time" style="font-size:15px;color:{C["sub"]};margin:0 0 14px">{E(sc["time"])}</p>'
                 if mode != "substack" else f"<p><strong>{E(sc['place'])}</strong><br><em>{E(sc['time'])}</em></p>")
        first = "".join(para(c, t, mode) for c, t in paras[:2])
        rest = "".join(para(c, t, mode) for c, t in paras[2:])
        fig = figure(SCENE_IMG[i], SCENE_ALT[i], SCENE_ALT[i], mode)
        if mode in ("wordpress", "tistory"):
            H.append(f'<div class="row"><div class="col">{intro}{first}</div>{fig}</div>{rest}')
        else:
            H.append(intro + fig + first + rest)
        if i == 3:
            H.append(figure("img_ep8_b52_41", "이륙하는 B-52, 2026년 3월 22일", "'장대한 분노' 작전 중 출격하는 미 공군 B-52 폭격기, 2026년 3월 22일", mode))
        if i == 5:
            H.append(figure("img_ep8_nicu", "신생아 집중치료실의 인큐베이터", "신생아 집중치료실 — 발전소가 꺼지면 가장 먼저 멎는 곳 가운데 하나", mode))
    H.append(para("", "— 8화 끝. 9화에서 계속됩니다. —", mode))
    # background knowledge
    H.append(n("h2", "배경 지식 — 나탄즈, 디모나, 그리고 전쟁법"))
    for q, a in HISTORY: H.append(n("h3", E(q)) + para("", a, mode))
    H.append(figure("img_ep8_natanz_pav", "나탄즈의 압바스아바드 정자", "이란 나탄즈의 압바스아바드 정자 — 핵시설로 알려진 이 지역의 역사 유적", mode))
    # fact vs fiction
    H.append(n("h2", "무엇이 사실이고 무엇이 창작인가"))
    if mode == "substack":
        H.append("<ul>" + "".join(f"<li><strong>{E(a)}</strong> ({E(b)}) — {E(c)}</li>" for a, b, c in FACT) + "</ul>")
    else:
        th = (lambda x: f'<th style="{ST["th"]}">{x}</th>') if mode == "naver" else (lambda x: f"<th>{x}</th>")
        td = (lambda x: f'<td style="{ST["td"]}">{x}</td>') if mode == "naver" else (lambda x: f"<td>{x}</td>")
        H.append((f'<table style="{ST["table"]}">' if mode == "naver" else "<table>") + f"<thead><tr>{th('항목')}{th('구분')}{th('설명')}</tr></thead><tbody>" +
                 "".join(f"<tr>{td(E(a))}{td(E(b))}{td(E(c))}</tr>" for a, b, c in FACT) + "</tbody></table>")
    # characters
    H.append(n("h2", "등장인물 현황 — 제8화 끝"))
    if mode == "substack":
        H.append("<ul>" + "".join(f"<li><strong>{E(a)}</strong> ({E(b)}) — {E(c)}</li>" for a, b, c in CHARS) + "</ul>")
    else:
        H.append("".join(para("", f"■ {a} ({b}) — {c}", mode) for a, b, c in CHARS))
    # FAQ
    H.append(n("h2", "자주 묻는 질문 (FAQ)"))
    if mode in ("wordpress", "tistory"):
        H.append('<dl class="faq">' + "".join(f"<dt>Q. {E(q)}</dt><dd>A. {E(a)}</dd>" for q, a in FAQ) + "</dl>")
    else:
        for q, a in FAQ: H.append(n("h3", "Q. " + E(q)) + para("", "A. " + a, mode))
    # next
    H.append(n("h2", "다음 화 예고 — 제9화"))
    H.append(para("", NEXT, mode))
    # sources
    H.append(n("h2", "출처"))
    src_items = [(a, u) for a, u in SOURCES]
    used = ["img_ep8_b52_42", "img_ep8_telaviv39"] + SCENE_IMG + ["img_ep8_b52_41", "img_ep8_nicu", "img_ep8_natanz_pav"]
    seen = []
    for k in used:
        if k in seen: continue
        seen.append(k); m = MAN[k]
        src_items.append((f"이미지 — {m['title']} — {credit_txt(k)}", m["page"]))
    lis = "".join(f'<li>{E(a)}<br><a href="{E(u)}"' + ('' if mode == "substack" else ' target="_blank" rel="noopener"') + f'>{E(u)}</a></li>' for a, u in src_items)
    H.append(f'<ol style="font-size:15px;line-height:1.7">{lis}</ol>' if mode == "naver" else f"<ol>{lis}</ol>")
    H.append(f'<div style="{ST["disc"]}">{E(DISCLAIMER)}</div>' if mode == "naver" else (f"<p><em>{E(DISCLAIMER)}</em></p>" if mode == "substack" else f'<div class="disc">{E(DISCLAIMER)}</div>'))
    if mode in ("naver", "tistory"):
        H.append(f'<p style="color:#555;font-size:16px">' + " ".join("#" + h for h in HASHTAGS) + "</p>")
    body = "\n".join(H)
    if mode == "substack":
        return body
    if mode == "naver":
        return f'<div style="{ST["wrap"]}">\n{body}\n</div>'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": TITLE[:110], "description": DESC, "inLanguage": "ko", "datePublished": POSTED, "dateModified": POSTED,
         "genre": "전쟁 소설(픽션)", "keywords": ", ".join(KEYWORDS), "image": [img_url("img_ep8_b52_42")],
         "author": {"@type": "Organization", "name": "장대한 분노 · SOULTHREAD"}, "isPartOf": {"@type": "CreativeWorkSeries", "name": "장대한 분노: 호르무즈의 밤"},
         "about": [{"@type": "Thing", "name": "2026 Iran war"}, {"@type": "Place", "name": "Natanz"}, {"@type": "Place", "name": "Dimona"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@type": "VideoObject", "name": "장대한 분노 제8화 「핵의 문턱」 4K 롱폼", "description": DESC, "thumbnailUrl": img_url("img_ep8_b52_42"),
         "uploadDate": POSTED, "contentUrl": VID + "epic_fury_ep08_longform_ko.mp4", "inLanguage": "ko"}]}
    head = (f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap">'
            f"<style>{CSS}</style>")
    return f"{head}\n<div class=\"efb\">\n{body}\n</div>\n<script type=\"application/ld+json\">{json.dumps(ld, ensure_ascii=False)}</script>"

def standalone(mode, body):
    """미리보기용 완전한 HTML(브라우저에서 바로 열기)."""
    extra = "" if mode in ("wordpress", "tistory") else f"<link rel='stylesheet' href='https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap'><style>body{{font-family:'Noto Sans KR',sans-serif;font-size:19px;line-height:1.9;max-width:860px;margin:0 auto;padding:16px}} img{{max-width:100%;height:auto}}</style>"
    return (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{E(TITLE)}</title><meta name='description' content='{E(DESC)}'><meta name='keywords' content='{E(', '.join(KEYWORDS))}'>"
            f"<meta property='og:title' content='{E(TITLE)}'><meta property='og:description' content='{E(DESC)}'><meta property='og:image' content='{img_url('img_ep8_b52_42')}'>"
            f"<meta property='og:type' content='article'>{extra}</head><body style='background:#fbf9f4;margin:0;padding:16px'>{body}</body></html>")

if __name__ == "__main__":
    for mode in ("wordpress", "tistory", "naver", "substack"):
        b = build(mode)
        open(f"{OUT}/epic_fury_ep08_blog_{mode}.html", "w").write(standalone(mode, b))
        open(f"{OUT}/epic_fury_ep08_blog_{mode}_body.html", "w").write(b)
        print(mode, len(b))
    meta = dict(title=TITLE, description=DESC, keywords=KEYWORDS, hashtags=HASHTAGS, slug="epic-fury-ep08-nuclear-threshold-natanz-dimona")
    json.dump(meta, open(f"{OUT}/epic_fury_ep08_blog_meta.json", "w"), ensure_ascii=False, indent=1)
