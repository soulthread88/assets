# -*- coding: utf-8 -*-
"""EPIC FURY platform MP4 — EP02 content (EN, U.S. style). Template v3: 21 pages = 5 news + 8 scenes x 2 screens."""
LANG = 'en'
EP_NO = "2"; EP2 = "02"
SUBTITLE = 'The Arithmetic of Decapitation'
DATE = 'Mar. 1, 2026'
BREAKING = ["Iran officially confirms Khamenei's death — 40 days of mourning, interim leadership council",
            "Tankers hit near Hormuz, about 150 ships stranded — six U.S. troops killed in Kuwait"]
TICKER = ["Mar. 1 — Tehran confirms Khamenei's death", "Mar. 1 — Synagogue hit in Beit Shemesh, 9 dead",
          "Mar. 1 — Two tankers hit, 150 ships stalled at Hormuz", "Mar. 2 — Hezbollah enters war, Qatar halts LNG",
          "Mar. 3 — Assembly of Experts hit, 787 dead"]
NEWS = [
 ('Tehran, Mar. 1',
  "On March 1 the Iranian government officially confirmed the death of Supreme Leader Ali Khamenei, a day after his residential compound was struck. It declared forty days of national mourning. Ali Larijani, secretary of the Supreme National Security Council, announced an interim leadership council to run the country until a successor was chosen. The bombing did not stop. The head was cut off. The body still stood.",
  'img_tehran_west'),
 ('Tehran · Beit Shemesh, Mar. 1',
  "The same day the Revolutionary Court building in Tehran was destroyed, and the Revolutionary Guards' Tharallah headquarters came down. Explosions went on near Azadi Square and Milad Tower. The Chinese-made HQ-9B batteries guarding the capital were reported neutralized. Iran fired back. A missile fell on a synagogue in Beit Shemesh, Israel, killing nine people and wounding sixty-five.",
  'vid_tehran_smoke'),
 ('Strait of Hormuz, Mar. 1',
  "Five nautical miles north of Khasab, Oman, the tanker Skylight was hit and four people were injured. Aboard the tanker MKD Vyom, one person was killed. Not a single mine had been laid. What stopped the ships was the insurers. With no war-risk cover, owners kept their tankers out. About 150 ships sat stalled in and around the strait, the channel that carries about a fifth of the world's oil.",
  'vid_sea_strait'),
 ('Haifa · Kuwait, Mar. 2',
  "On March 2 Hezbollah fired rockets at Haifa. Israel called it an official declaration of war and struck Beirut. Entrance buildings at the Natanz nuclear site were hit. QatarEnergy halted LNG production after two of its gas facilities were attacked. At Shuaiba Port in Kuwait, an Iranian drone attack killed six U.S. service members. They were the first Americans killed in this war.",
  'vid_lincoln'),
 ('Tehran, Mar. 3',
  "On March 3 the building of the Assembly of Experts, the body that chooses the Supreme Leader, was bombed, along with the Supreme National Security Council building. The Qajar-era Golestan Palace was damaged by a strike nearby. CENTCOM said 17 Iranian vessels had been destroyed. The Iranian Red Crescent put the death toll at 787. Israel approved a ground operation in Lebanon. Day four, and the front kept widening.",
  'img_borujerdi4'),
]
SCENES = [
 ('Langley, Virginia · CIA Iran Operations Center', 'Fordow Was Alive',
  "The screen changed first. March 1, 3:12 a.m., Langley. Dr. Leila Shirazi was setting down her third coffee when her hand stopped. The signal channel for the Fordow nuclear site. In June 2025, six B-2s had dropped twelve bunker busters on it. Officially it was a dead facility. But a signal came up. Every 5.7 seconds. Steady as a pulse.",
  "The centrifuges were turning. She called over the partition. \"Sam. Come here now.\" Senior satellite analyst Sam Farrell looked and swore under his breath. The vibration was regular. Not a collapsing tunnel. That period was the operating frequency of an IR-6 centrifuge. Somebody had brought the dead machines back to life, and had decided not to shut them off. She titled the report in three words. Fordow, confirmation requested.",
  'vid_monitors', 'vid_control_room'),
 ('Alborz Mountains, Iran · air-defense command post', 'Who Speaks to Us Now',
  "The dead man's name finally came over state television. Col. Darius Sepahvand stood in front of an old TV. A black band across the screen. A reading from the Koran. The martyrdom of the Supreme Leader and forty days of mourning. For thirty-one years he had guarded the sky. Now the sky belonged to someone else. No batteries were left to take an order to intercept. Nobody was left to give it.",
  "The young officers looked at him. Eyes waiting for orders. Under the grief and the anger was the thing nobody said. Who speaks to us now? You fire missiles and they run out. On the day they ran out, what would they answer with? He thought of his daughter, Narges, west of Tehran. He had not reached her since yesterday. The head was cut off. The body still stood, waiting for orders.",
  'vid_radar', 'img_borujerdi8'),
 ('Mina Salman Port, Bahrain · U.S. Fifth Fleet', 'The Longest Ninety Seconds',
  "Lt. Kim Junho was in the restroom when the missile sirens went off. Twenty-nine, a South Korean Navy liaison officer. He had never seen real war. Not until yesterday morning. He ran into the corridor and down to the underground command center. On the target-analysis screen, Mina Salman Port came up. The place where he was standing. The next ninety seconds would be the longest of his life.",
  "The Patriot batteries fired again and again. Shock waves shook the floor. He was holding on to the leg of a desk. His hands were shaking. Nearly all of them were intercepted. Nearly. When the alert lifted he worked out the time in Seoul. Eight-thirty at night. His mother would have the news on. He did not call. He was afraid they would hear his voice shake. \"You okay?\" \"Yes.\" It was a lie. It was also true.",
  'vid_dark_sky', 'vid_lincoln'),
 ('Tehran · Valiasr Avenue', 'The One With the Gun Stops Too',
  "The sky over Tehran was black. But the streets were not quiet. On the afternoon Khamenei's death was confirmed, people gathered on Valiasr Avenue. \"Freedom! Freedom! Iran is free!\" At first a few dozen. Thirty minutes later, a few hundred. They threw off their hijabs. What had been pressed down in their throats for forty-seven years came out ahead of the bombs. Then the Basij came.",
  "Tear gas first. Then batons. Somewhere in an alley a shot went off. Soraya Tahir, a twenty-two-year-old engineering student, was in that street. Right in front of her, a young militiaman got off a motorcycle and stopped. His baton came down. The look on his face said: I don't know either. He's a person too. The one with the gun is a person too. Bombs do not stop. People can.",
  'vid_azadi', 'vid_azadi_dusk'),
 ('Eastern Mediterranean · bridge, USS Gerald R. Ford', 'Six',
  "March 2, dawn, the eastern Mediterranean. Shadows had settled under Capt. Marcus Webb's eyes. He had not slept six hours since the war began. Overnight Hezbollah had entered the war, and past the horizon Israeli jets were hitting Beirut. But Webb's eyes were on another sea a thousand miles away. Hormuz was closed. And in Kuwait, six American service members had been killed.",
  "Six. He read the number twice. No names yet. Twice in twenty-five years he had been the one who knocks on the family's door. War correspondent Sarah Callahan stood beside him. \"I filed a story about a girl named Nariman. She's alive. Her mother found her under the concrete.\" Then, quietly: \"It was our bomb that did it.\" He did not answer. Not answering was the answer.",
  'img_ford_ep2', 'img_ford_ep2'),
 ('University of Tehran · Department of Philosophy', 'The Last Page, Fifty-Three Years Later',
  "For the first time in fifty-three years, Professor Azad Moradi opened his desk drawer. At the bottom lay a notebook he had bought in 1973. On the first page, in his hand: Truth is uncomfortable. But a lie hurts longer. Black smoke stood outside the window. Word came that Golestan Palace had been damaged. What was close was the singing. Students in the courtyard, without hijabs. The first time in forty-seven years.",
  "On the last blank page he wrote. Khamenei is dead. I do not grieve his death. Whether that is betrayal or truth, I do not know. Outside the window the students are singing. And I, a seventy-two-year-old philosopher, am crying. Why? Perhaps that is the answer. A bomb breaks something and is done. A song is the will to build something. If the will to build is left, hope is left.",
  'img_golestan', 'img_golestan'),
 ('Langley, Virginia · CIA emergency conference room', 'Eighty-Five Percent',
  "March 3, morning. Fifty-one hours after Leila filed her report, a meeting was called. Seven people in the room. Leila gave the conclusion. Better than an 85 percent probability that some centrifuge halls under Fordow are still operating. The room went quiet. \"Meaning last June's strike was incomplete?\" \"Meaning the reason it wasn't on the list just went away,\" Sam said.",
  "\"Are you recommending another strike?\" somebody asked. \"That's not mine to decide. I give you the information.\" It was true. But she knew it was her information that made the decision. After the meeting, through the window at the end of the corridor, she saw the blue Virginia sky. Sixty-three hundred miles away, the sky over Tehran was black. We believe we can beat an enemy we have never understood.",
  'vid_analyst', 'vid_sky_blue'),
 ('Tehran · Valiasr Avenue', 'Blue Between the Smoke',
  "Soraya Tahir had gone into the street twice. Once it put her in prison. Once she saw a Basij man stop. She looked up. The sky was black. Columns of smoke hid the sun. But there was a gap in the smoke. Through it you could see blue. Just a little. But you could see it.",
  "That blue is the same sky as this one. The sky over Tehran, the sky over Langley, the sky over Tel Aviv. In the end it's one sky. Under it one person runs machines, one fires missiles, one sings. As long as that blue is there, I can't give up. Even if I can't say why. Would the gap still be open tomorrow?",
  'vid_sky_clouds', 'vid_tehran_dawn'),
]
PAGES = []
for i, (loc, cap, m) in enumerate(NEWS, 1):
    PAGES.append(dict(n=i, kind="news", loc=loc, text=cap, media=m))
for j, (tag, h2, p1, p2, m1, m2) in enumerate(SCENES):
    n = 6 + 2 * j
    PAGES.append(dict(n=n, kind="novel", tag=tag, h2=h2, text=p1, media=m1, alt=False))
    PAGES.append(dict(n=n + 1, kind="novel", tag=tag, h2=None, text=p2, media=m2, alt=(m1 == m2), end=(n + 1 == 21)))
END_NOTE = '— End of Episode 2. Continued in Episode 3. —'
PLATFORMS = {
 'longform': (3840, 2160, list(range(1, 22)), 'wide', 'The Arithmetic of Decapitation', 'Epic Fury · Episode 2', 'img_ford_ep2'),
 'longform_mobile': (2160, 3840, list(range(1, 22)), 'band', 'The Arithmetic of Decapitation', 'Epic Fury · Episode 2 · Mobile', 'img_ford_ep2'),
 'x': (3840, 2160, [1, 2, 3], 'wide', "Khamenei's Death Confirmed", 'Epic Fury · Episode 2', 'img_tehran_west'),
 'facebook': (3840, 2160, [1, 6, 7], 'wide', 'Fordow Was Alive', 'Epic Fury · Episode 2', 'vid_monitors'),
 'shorts': (2160, 3840, [1, 2, 3, 4, 5], 'band', 'The Head Is Gone. The War Goes On.', 'Epic Fury · Episode 2', 'img_tehran_west'),
 'reels': (2160, 3840, [12, 13, 16, 17], 'band', 'The One With the Gun Stops Too', 'Epic Fury · Episode 2', 'vid_azadi'),
 'tiktok': (2160, 3840, [1, 6, 7, 18, 19], 'band', 'The Machines They Called Dead', 'Epic Fury · Episode 2', 'vid_analyst'),
 'threads': (2160, 2700, [1, 10, 11, 14, 15], 'band', 'The Longest Ninety Seconds', 'Epic Fury · Episode 2', 'vid_lincoln'),
 'feeds': (2160, 2700, [20, 21], 'band', 'Blue Between the Smoke', 'Epic Fury · Episode 2', 'vid_sky_clouds'),
}
END_TITLE = 'Continued in Episode 3'; END_SUB = 'Fiction · AI narration'; END_MEDIA = "vid_sunset_sea"
END_NARR = 'Epic Fury continues in Episode 3.'
UI = {'html_lang': 'en', 'brand_left': 'WAR NOVEL', 'l1': 'Epic Fury', 'l2': 'Night Over Hormuz', 'headline': 'Episode 2 — The Arithmetic of Decapitation', 'ep_badge': 'EP 02', 'sit': 'SITUATION REPORT', 'breaking': 'FICTION BREAKING', 'ticker': 'KEY EVENTS', 'cover_top': 'EPIC FURY · NIGHT OVER HORMUZ', 'cover_kind': 'NOVEL', 'disclaimer': 'A novel inspired by real events. Characters and dialogue are invented.', 'title': 'Epic Fury: Night Over Hormuz — Episode 2: The Arithmetic of Decapitation', 'rep': 'Replace', 'dele': 'Delete', 'aria': 'Play narration', 'novideo': 'Your browser does not support embedded video.', 'light': '☀ Light', 'dark': '🌙 Dark', 'fictional': 'a fictional event'}

import re as _re
def _smart(s):
    s = _re.sub(r'(^|[\s(\[—])"', '\\1“', s); s = s.replace('"', '”')
    s = _re.sub(r"(^|[\s(\[—“])'", "\\1‘", s); s = s.replace("'", "’")
    return s
for _p in PAGES:
    for _k in ("text", "loc", "tag", "h2"):
        if _p.get(_k): _p[_k] = _smart(_p[_k])
BREAKING = [_smart(x) for x in BREAKING]; TICKER = [_smart(x) for x in TICKER]
PLATFORMS = {k: v[:4] + (_smart(v[4]), _smart(v[5])) + v[6:] for k, v in PLATFORMS.items()}
