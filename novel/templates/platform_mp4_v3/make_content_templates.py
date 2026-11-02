# -*- coding: utf-8 -*-
"""Write content_epXX_{ko,en,jp}.py — the fill-in content files for the platform MP4 template v3.
Structure = EP01 final (21 pages: 5 news + 8 scenes x 2). Text in [[...]] is a placeholder to replace;
media keys are EP01 samples from media/manifest.json, to be replaced with the episode's own media keys."""
import os, json
OUT = os.path.join(os.path.dirname(__file__), "content")
NEWS_MEDIA = ["img_b2_prep", "img_spruance", "vid_phone", "vid_dark_sky", "img_map100h"]
SCENE_MEDIA = [("vid_azadi", "vid_sky_blue"), ("vid_control_room", "vid_monitors"), ("vid_radar", "vid_phone"),
               ("img_ford_deck", "img_ford_deck"), ("vid_analyst", "vid_analyst"), ("img_borujerdi8", "img_borujerdi4"),
               ("vid_tehran_smoke", "vid_azadi_dusk"), ("vid_carrier_sea", "vid_sunset_sea")]
# default page picks per platform = EP01 final (change per episode: choose the pages that carry that platform's hook)
PICKS = {"longform": "list(range(1, 22))", "longform_mobile": "list(range(1, 22))", "x": "[1, 2, 3]", "facebook": "[1, 6, 7]",
         "shorts": "[1, 2, 3, 4, 5]", "reels": "[8, 9, 18, 19]", "tiktok": "[3, 16, 17, 20, 21]", "threads": "[1, 12, 13, 14, 15]", "feeds": "[10, 11]"}
SIZE = {"longform": (3840, 2160, "wide"), "longform_mobile": (2160, 3840, "band"), "x": (3840, 2160, "wide"), "facebook": (3840, 2160, "wide"),
        "shorts": (2160, 3840, "band"), "reels": (2160, 3840, "band"), "tiktok": (2160, 3840, "band"), "threads": (2160, 2700, "band"), "feeds": (2160, 2700, "band")}
COVER_MEDIA = {"longform": "img_ford_deck", "longform_mobile": "img_ford_deck", "x": "img_b2_prep", "facebook": "vid_azadi", "shorts": "img_spruance",
               "reels": "vid_tehran_smoke", "tiktok": "img_borujerdi8", "threads": "img_ford_deck", "feeds": "vid_radar"}
L10N = {
 "ko": dict(header="KO", date="[[YYYY.MM.DD]]", ep_word="화",
            ui=dict(html_lang="ko", brand_left="전쟁소설", l1="장대한 분노", l2="호르무즈의 밤", headline="제 [[화수]]화 - [[부제목]]",
                    ep_badge="EP [[화수 두자리]]", sit="실전 상황", breaking="소설 속보", ticker="주요사건 타임라인",
                    cover_top="장대한 분노 · 호르무즈의 밤", cover_kind="소설", disclaimer="실제 사건에서 착상한 소설입니다. 등장인물과 대화는 창작입니다.",
                    title="장대한 분노 - 호르무즈의 밤 — 제[[화수]]화 [[부제목]]", rep="교체", dele="삭제", aria="내레이션 재생",
                    novideo="동영상을 지원하지 않는 브라우저입니다.", light="☀ Light", dark="🌙 Dark", fictional="소설 속 가상 사건"),
            end_note="— [[화수]]화 끝. [[다음 화수]]화에서 계속됩니다. —", end_title="[[다음 화수]]화에서 계속됩니다", end_sub="픽션 · AI 내레이션",
            end_narr="장대한 분노, [[다음 화수]]화에서 계속됩니다.", cover_sub="장대한 분노 EP[[화수 두자리]]", mobile_sub="장대한 분노 EP[[화수 두자리]] · 모바일"),
 "en": dict(header="EN (U.S. style: Feb. 28, 2026 · 9:45 a.m. · curly quotes)", date="[[Mon. D, YYYY]]", ep_word="Episode",
            ui=dict(html_lang="en", brand_left="WAR NOVEL", l1="Epic Fury", l2="Night Over Hormuz", headline="Episode [[N]] — [[Subtitle]]",
                    ep_badge="EP [[NN]]", sit="SITUATION REPORT", breaking="FICTION BREAKING", ticker="KEY EVENTS",
                    cover_top="EPIC FURY · NIGHT OVER HORMUZ", cover_kind="NOVEL", disclaimer="A novel inspired by real events. Characters and dialogue are invented.",
                    title="Epic Fury: Night Over Hormuz — Episode [[N]]: [[Subtitle]]", rep="Replace", dele="Delete", aria="Play narration",
                    novideo="Your browser does not support embedded video.", light="☀ Light", dark="🌙 Dark", fictional="a fictional event"),
            end_note="— End of Episode [[N]]. Continued in Episode [[N+1]]. —", end_title="Continued in Episode [[N+1]]", end_sub="Fiction · AI narration",
            end_narr="Epic Fury continues in Episode [[N+1]].", cover_sub="Epic Fury · Episode [[N]]", mobile_sub="Epic Fury · Episode [[N]] · Mobile"),
 "jp": dict(header="JP (日本式: 2026年2月28日 · 午前9時45分 · 「」)", date="[[YYYY年M月D日]]", ep_word="話",
            ui=dict(html_lang="ja", brand_left="戦争小説", l1="エピック・フューリー", l2="ホルムズの夜", headline="第[[N]]話 ― [[副題]]",
                    ep_badge="EP [[NN]]", sit="戦況", breaking="小説速報", ticker="主な出来事",
                    cover_top="エピック・フューリー · ホルムズの夜", cover_kind="小説", disclaimer="実際の戦争から着想を得たフィクションです。登場人物と会話は創作です。",
                    title="エピック・フューリー：ホルムズの夜 ― 第[[N]]話 [[副題]]", rep="差し替え", dele="削除", aria="ナレーション再生",
                    novideo="お使いのブラウザは動画に対応していません。", light="☀ ライト", dark="🌙 ダーク", fictional="作中の架空の出来事"),
            end_note="― 第[[N]]話 終わり。第[[N+1]]話へ続く ―", end_title="第[[N+1]]話へ続く", end_sub="フィクション · AIナレーション",
            end_narr="エピック・フューリー、第[[N+1]]話へ続く。", cover_sub="エピック・フューリー 第[[N]]話", mobile_sub="エピック・フューリー 第[[N]]話 · モバイル"),
}
PH = {"ko": dict(sub="[[부제목]]", brk="[[속보 헤드라인 {i}]]", tk="[[타임라인 {i}: 시각 + 사건]]", loc="[[속보 {i}: 장소, 시각]]",
                 cap="[[속보 {i}: 화면 문장 = 내레이션, 200~260자]]", tag="[[장면 {i}: 장소 · 위치]]", h2="[[장면 {i}: 소제목]]",
                 p1="[[장면 {i} 첫 화면: 본문 = 내레이션, 200~240자]]", p2="[[장면 {i} 둘째 화면: 본문 = 내레이션, 200~240자]]", cover="[[{p} 표지 제목]]"),
      "en": dict(sub="[[Subtitle]]", brk="[[Breaking headline {i}]]", tk="[[Timeline {i}: time — event]]", loc="[[News {i}: place · time]]",
                 cap="[[News {i}: on-screen text = narration, 380–440 characters]]", tag="[[Scene {i}: place · location]]", h2="[[Scene {i}: title]]",
                 p1="[[Scene {i}, screen 1: body = narration, 330–400 characters]]", p2="[[Scene {i}, screen 2: body = narration, 330–400 characters]]", cover="[[{p} cover title]]"),
      "jp": dict(sub="[[副題]]", brk="[[速報見出し {i}]]", tk="[[タイムライン {i}: 時刻 + 出来事]]", loc="[[速報 {i}: 場所 · 時刻]]",
                 cap="[[速報 {i}: 画面の文 = ナレーション、170~220字]]", tag="[[場面 {i}: 場所 · 位置]]", h2="[[場面 {i}: 小見出し]]",
                 p1="[[場面 {i} 1画面目: 本文 = ナレーション、160~200字]]", p2="[[場面 {i} 2画面目: 本文 = ナレーション、160~200字]]", cover="[[{p} 表紙タイトル]]")}
for lang, Lx in L10N.items():
    P = PH[lang]; r = repr
    lines = [f'# -*- coding: utf-8 -*-',
             f'"""EPIC FURY 플랫폼 MP4 템플릿 v3 — 내용 파일 ({Lx["header"]}).',
             '[[...]] 자리를 이번 화 내용으로 바꾸고, 미디어 키(img_/vid_)는 media/manifest.json에 등록한 이번 화 미디어로 바꾼다.',
             '구조는 EP01 최종본과 같다: 21쪽 = 속보 5쪽 + 장면 8개 × 2화면. 화면 문장이 곧 내레이션이다."""',
             f'LANG = {r(lang)}', 'EP_NO = "[[화수]]"; EP2 = "[[화수 두자리]]"', f'SUBTITLE = {r(P["sub"])}', f'DATE = {r(Lx["date"])}',
             f'BREAKING = {r([P["brk"].format(i=i) for i in (1, 2)])}', f'TICKER = {r([P["tk"].format(i=i) for i in range(1, 6)])}',
             'NEWS = [  # (위치·시각, 화면 문장 = 내레이션, 미디어 키)']
    for i in range(1, 6):
        lines.append(f' ({r(P["loc"].format(i=i))}, {r(P["cap"].format(i=i))}, {r(NEWS_MEDIA[i-1])}),')
    lines.append(']\nSCENES = [  # (장면 위치, 소제목, 첫 화면 본문, 둘째 화면 본문, 미디어1, 미디어2 — 같은 미디어면 둘째 화면은 3초 뒤부터 확대해 보여 준다)')
    for i in range(1, 9):
        m1, m2 = SCENE_MEDIA[i-1]
        lines.append(f' ({r(P["tag"].format(i=i))}, {r(P["h2"].format(i=i))}, {r(P["p1"].format(i=i))}, {r(P["p2"].format(i=i))}, {r(m1)}, {r(m2)}),')
    lines += [']', 'PAGES = []', 'for i, (loc, cap, m) in enumerate(NEWS, 1):', '    PAGES.append(dict(n=i, kind="news", loc=loc, text=cap, media=m))',
              'for j, (tag, h2, p1, p2, m1, m2) in enumerate(SCENES):', '    n = 6 + 2 * j',
              '    PAGES.append(dict(n=n, kind="novel", tag=tag, h2=h2, text=p1, media=m1, alt=False))',
              '    PAGES.append(dict(n=n + 1, kind="novel", tag=tag, h2=None, text=p2, media=m2, alt=(m1 == m2), end=(n + 1 == 21)))',
              f'END_NOTE = {r(Lx["end_note"])}',
              '# 플랫폼: (가로, 세로, 쪽 번호, 배치 wide=16:9 원본 화면 / band=세로 띠, 표지 제목, 표지 부제, 표지 미디어)',
              'PLATFORMS = {']
    for p, (w, h, lay) in SIZE.items():
        sub = Lx["mobile_sub"] if p == "longform_mobile" else Lx["cover_sub"]
        lines.append(f' {r(p)}: ({w}, {h}, {PICKS[p]}, {r(lay)}, {r(P["cover"].format(p=p))}, {r(sub)}, {r(COVER_MEDIA[p])}),')
    lines += ['}', f'END_TITLE = {r(Lx["end_title"])}; END_SUB = {r(Lx["end_sub"])}; END_MEDIA = "vid_sunset_sea"', f'END_NARR = {r(Lx["end_narr"])}',
              f'UI = {r(Lx["ui"])}']
    open(os.path.join(OUT, f"content_epXX_{lang}.py"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("wrote", lang)
