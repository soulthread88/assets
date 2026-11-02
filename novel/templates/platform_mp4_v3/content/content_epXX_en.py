# -*- coding: utf-8 -*-
"""EPIC FURY 플랫폼 MP4 템플릿 v3 — 내용 파일 (EN (U.S. style: Feb. 28, 2026 · 9:45 a.m. · curly quotes)).
[[...]] 자리를 이번 화 내용으로 바꾸고, 미디어 키(img_/vid_)는 media/manifest.json에 등록한 이번 화 미디어로 바꾼다.
구조는 EP01 최종본과 같다: 21쪽 = 속보 5쪽 + 장면 8개 × 2화면. 화면 문장이 곧 내레이션이다."""
LANG = 'en'
EP_NO = "[[화수]]"; EP2 = "[[화수 두자리]]"
SUBTITLE = '[[Subtitle]]'
DATE = '[[Mon. D, YYYY]]'
BREAKING = ['[[Breaking headline 1]]', '[[Breaking headline 2]]']
TICKER = ['[[Timeline 1: time — event]]', '[[Timeline 2: time — event]]', '[[Timeline 3: time — event]]', '[[Timeline 4: time — event]]', '[[Timeline 5: time — event]]']
NEWS = [  # (위치·시각, 화면 문장 = 내레이션, 미디어 키)
 ('[[News 1: place · time]]', '[[News 1: on-screen text = narration, 380–440 characters]]', 'img_b2_prep'),
 ('[[News 2: place · time]]', '[[News 2: on-screen text = narration, 380–440 characters]]', 'img_spruance'),
 ('[[News 3: place · time]]', '[[News 3: on-screen text = narration, 380–440 characters]]', 'vid_phone'),
 ('[[News 4: place · time]]', '[[News 4: on-screen text = narration, 380–440 characters]]', 'vid_dark_sky'),
 ('[[News 5: place · time]]', '[[News 5: on-screen text = narration, 380–440 characters]]', 'img_map100h'),
]
SCENES = [  # (장면 위치, 소제목, 첫 화면 본문, 둘째 화면 본문, 미디어1, 미디어2 — 같은 미디어면 둘째 화면은 3초 뒤부터 확대해 보여 준다)
 ('[[Scene 1: place · location]]', '[[Scene 1: title]]', '[[Scene 1, screen 1: body = narration, 330–400 characters]]', '[[Scene 1, screen 2: body = narration, 330–400 characters]]', 'vid_azadi', 'vid_sky_blue'),
 ('[[Scene 2: place · location]]', '[[Scene 2: title]]', '[[Scene 2, screen 1: body = narration, 330–400 characters]]', '[[Scene 2, screen 2: body = narration, 330–400 characters]]', 'vid_control_room', 'vid_monitors'),
 ('[[Scene 3: place · location]]', '[[Scene 3: title]]', '[[Scene 3, screen 1: body = narration, 330–400 characters]]', '[[Scene 3, screen 2: body = narration, 330–400 characters]]', 'vid_radar', 'vid_phone'),
 ('[[Scene 4: place · location]]', '[[Scene 4: title]]', '[[Scene 4, screen 1: body = narration, 330–400 characters]]', '[[Scene 4, screen 2: body = narration, 330–400 characters]]', 'img_ford_deck', 'img_ford_deck'),
 ('[[Scene 5: place · location]]', '[[Scene 5: title]]', '[[Scene 5, screen 1: body = narration, 330–400 characters]]', '[[Scene 5, screen 2: body = narration, 330–400 characters]]', 'vid_analyst', 'vid_analyst'),
 ('[[Scene 6: place · location]]', '[[Scene 6: title]]', '[[Scene 6, screen 1: body = narration, 330–400 characters]]', '[[Scene 6, screen 2: body = narration, 330–400 characters]]', 'img_borujerdi8', 'img_borujerdi4'),
 ('[[Scene 7: place · location]]', '[[Scene 7: title]]', '[[Scene 7, screen 1: body = narration, 330–400 characters]]', '[[Scene 7, screen 2: body = narration, 330–400 characters]]', 'vid_tehran_smoke', 'vid_azadi_dusk'),
 ('[[Scene 8: place · location]]', '[[Scene 8: title]]', '[[Scene 8, screen 1: body = narration, 330–400 characters]]', '[[Scene 8, screen 2: body = narration, 330–400 characters]]', 'vid_carrier_sea', 'vid_sunset_sea'),
]
PAGES = []
for i, (loc, cap, m) in enumerate(NEWS, 1):
    PAGES.append(dict(n=i, kind="news", loc=loc, text=cap, media=m))
for j, (tag, h2, p1, p2, m1, m2) in enumerate(SCENES):
    n = 6 + 2 * j
    PAGES.append(dict(n=n, kind="novel", tag=tag, h2=h2, text=p1, media=m1, alt=False))
    PAGES.append(dict(n=n + 1, kind="novel", tag=tag, h2=None, text=p2, media=m2, alt=(m1 == m2), end=(n + 1 == 21)))
END_NOTE = '— End of Episode [[N]]. Continued in Episode [[N+1]]. —'
# 플랫폼: (가로, 세로, 쪽 번호, 배치 wide=16:9 원본 화면 / band=세로 띠, 표지 제목, 표지 부제, 표지 미디어)
PLATFORMS = {
 'longform': (3840, 2160, list(range(1, 22)), 'wide', '[[longform cover title]]', 'Epic Fury · Episode [[N]]', 'img_ford_deck'),
 'longform_mobile': (2160, 3840, list(range(1, 22)), 'band', '[[longform_mobile cover title]]', 'Epic Fury · Episode [[N]] · Mobile', 'img_ford_deck'),
 'x': (3840, 2160, [1, 2, 3], 'wide', '[[x cover title]]', 'Epic Fury · Episode [[N]]', 'img_b2_prep'),
 'facebook': (3840, 2160, [1, 6, 7], 'wide', '[[facebook cover title]]', 'Epic Fury · Episode [[N]]', 'vid_azadi'),
 'shorts': (2160, 3840, [1, 2, 3, 4, 5], 'band', '[[shorts cover title]]', 'Epic Fury · Episode [[N]]', 'img_spruance'),
 'reels': (2160, 3840, [8, 9, 18, 19], 'band', '[[reels cover title]]', 'Epic Fury · Episode [[N]]', 'vid_tehran_smoke'),
 'tiktok': (2160, 3840, [3, 16, 17, 20, 21], 'band', '[[tiktok cover title]]', 'Epic Fury · Episode [[N]]', 'img_borujerdi8'),
 'threads': (2160, 2700, [1, 12, 13, 14, 15], 'band', '[[threads cover title]]', 'Epic Fury · Episode [[N]]', 'img_ford_deck'),
 'feeds': (2160, 2700, [10, 11], 'band', '[[feeds cover title]]', 'Epic Fury · Episode [[N]]', 'vid_radar'),
}
END_TITLE = 'Continued in Episode [[N+1]]'; END_SUB = 'Fiction · AI narration'; END_MEDIA = "vid_sunset_sea"
END_NARR = 'Epic Fury continues in Episode [[N+1]].'
UI = {'html_lang': 'en', 'brand_left': 'WAR NOVEL', 'l1': 'Epic Fury', 'l2': 'Night Over Hormuz', 'headline': 'Episode [[N]] — [[Subtitle]]', 'ep_badge': 'EP [[NN]]', 'sit': 'SITUATION REPORT', 'breaking': 'FICTION BREAKING', 'ticker': 'KEY EVENTS', 'cover_top': 'EPIC FURY · NIGHT OVER HORMUZ', 'cover_kind': 'NOVEL', 'disclaimer': 'A novel inspired by real events. Characters and dialogue are invented.', 'title': 'Epic Fury: Night Over Hormuz — Episode [[N]]: [[Subtitle]]', 'rep': 'Replace', 'dele': 'Delete', 'aria': 'Play narration', 'novideo': 'Your browser does not support embedded video.', 'light': '☀ Light', 'dark': '🌙 Dark', 'fictional': 'a fictional event'}
