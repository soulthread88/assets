# -*- coding: utf-8 -*-
"""EPIC FURY platform MP4 — EP07 content (EN, U.S. style). Template v3: 21 pages = 5 news + 8 scenes x 2 screens.
EP07 has nine scenes: scenes 1-7 get two screens; the last two screens go to scene 8 (Nowruz) and scene 9 (the aunt's call)."""
LANG = 'en'
EP_NO = "7"; EP2 = "07"
SUBTITLE = 'Fire at South Pars'
DATE = 'Mar. 18, 2026'
BREAKING = ["Israel bombs South Pars, the world's largest gas field — Iranian missiles hit Qatar's Ras Laffan",
            "About 20,000 seafarers trapped in the Gulf — Nowruz arrives under bombing, 640 strikes in a day"]
TICKER = ["Mar. 18 — Israel kills Intelligence Minister Khatib", "Mar. 18 — South Pars and Asaluyeh bombed; 12% of Iran's gas output hit",
          "Mar. 18 — Iranian missiles cause \"extensive damage\" at Ras Laffan; oil at $108", "Mar. 19 — Haifa and Kuwait refineries hit; U.S. F-35 makes emergency landing",
          "Mar. 20 — Nowruz; missile debris falls in Jerusalem's Old City"]
NEWS = [
 ('Asaluyeh, Mar. 18',
  "At 2:10 p.m. on March 18 the Israeli Air Force bombed South Pars, the world's largest gas field, and the refineries at Asaluyeh. Two processing plants stopped, and 12 percent of Iran's gas output was hit. Iran cut the gas it sent to Iraq. The strike was confirmed as coordinated and approved by the United States. The war had crossed the energy line.",
  'img_f22'),
 ('Ras Laffan · Riyadh · Abu Dhabi, Mar. 18',
  "Hours later Iranian missiles fell on the other side of the same gas field, at Ras Laffan in Qatar. QatarEnergy reported extensive damage, and Qatar expelled Iran's military attachés. Saudi Arabia intercepted six ballistic missiles, and Abu Dhabi shut down a gas facility. Oil jumped from $103 to $108 a barrel in a single day.",
  'vid_bainbridge'),
 ('Tehran · Washington, Mar. 18',
  "Before dawn the same day an Israeli night strike killed Iran's intelligence minister, Esmaeil Khatib. In Tehran thousands followed Larijani's funeral procession. In Washington President Trump said he had known nothing about the attack, then later said he had known and told Israel not to do it. There would be no more strikes on Iran's energy facilities, he said.",
  'img_tehran_mar18'),
 ('Hormuz · Haifa · Kuwait, Mar. 19',
  "The International Maritime Organization said about 3,200 ships and 20,000 seafarers were trapped west of the strait. On March 19 U.S. forces began air operations over the strait against Iranian boats and drones. The same day the Mina al-Ahmadi refinery in Kuwait and the BAZAN refinery in Haifa were hit. A U.S. F-35 was struck over Iran and made an emergency landing.",
  'img_john_finn'),
 ('Tehran · Jerusalem, Mar. 20',
  "At 6:16 p.m. on March 20, Nowruz, the Iranian new year, arrived under bombing. A human rights group logged 640 airstrikes across 17 provinces that day. A Revolutionary Guards spokesman was killed. Iran fired nine ballistic missiles at Jerusalem, and debris fell 400 meters from the Western Wall. The new Supreme Leader still had not shown his face.",
  'img_eid'),
]
SCENES = [
 ('Asaluyeh, Iran · South Pars gas processing complex', 'The Heart',
  "It was midday. The sun was so bright that at first he could not see the fire. Reza Karimi was a control-room technician at Phase 4. Gas rising from 3,000 meters under the sea was washed and split here and warmed half the country. He did not call this place a plant. He called it the heart. The surface of his tea trembled first. Then the floor. Then the sound.",
  "A coworker pulled him into an evacuation truck. He looked back. The plant whose every valve he knew by its habits stood inside an orange column. Its gas went to hospital boilers, bread ovens, his mother's stove. The ones who dropped the bombs called it the Guards' cash machine. But whoever aims at the heart says he is aiming at the fist. When the heart stops, it is not only the fist that goes cold.",
  'vid_tehran_smoke', 'vid_dust'),
 ('Qatar · Ras Laffan Industrial City', 'Write Only What You Saw',
  "Park Jeongwoo was an engineer a Korean engineering company had sent to this desert. One in five tanks of the liquefied gas the world uses was loaded at these docks. At night the flare stacks stood like lighthouses, which meant someone's winter on the far side of the earth was warm, apartments in Seoul among them. In the afternoon word came that Asaluyeh was burning. Everyone knew where the answer would come. The alarm went off.",
  "In the shelter, messages from headquarters in Seoul poured in. Status report. Damage assessment. Headcount. Whether anyone was all right came on the last line. A stack fire does not spread like that. \"What do we report to Seoul?\" \"All personnel evacuated. Fire visually confirmed. Equipment damage unconfirmed. What you don't know, say you don't know. Write only what you saw. Seoul sets the price of gas from one line we write.\"",
  'vid_dark_sky', 'vid_control_room'),
 ("Tehran · Professor Azad Moradi's apartment", 'A Country Peeled Away',
  "Another explosion. He was used to it now. That was what was strange. People get used to the sound of explosions. It was the quietest violence war does to people. On the radio the announcer's voice shook. Intelligence Minister Khatib was dead. Azad was not a man to mourn him. That ministry had taken two of his students, and one had not come back. What he felt was vertigo at the speed of it.",
  "Out the window passed the black clothes following Larijani's coffin. They had finished their doctorates the same year. Both read Kant; one went to the lecture hall, the other to power. They had never liked each other. But one fewer person in this country could discuss the Critique of Pure Reason in Persian. The country was being peeled away from the top, layer by layer. What would rise from beneath, no one could see.",
  'img_tehran_mar18', 'img_tehran_west'),
 ('Langley, Virginia · CIA Iran Operations Center', 'Sentences That Cross',
  "On Dr. Leila Shirazi's screen, the things one man had said that day sat side by side. Knew nothing about it. Israel hit it out of anger. Knew, and told them not to. Read in any order, they did not make one man's day. When an enemy's words contradict each other, the analyst looks for the truth in the gap. When her own president's words did, no one had taught her what to look for.",
  "Three months ago, at a target review, she had raised her hand. Hit this and Iranians won't get through the winter. The minutes said: analyst's view noted. That one line was the grave of her view. On one side of her screen were the roofs of Evin. Nineteen days without reaching her aunt. A roof still standing, and someone alive under it. The satellite did not close that distance.",
  'vid_monitors', 'vid_analyst'),
 ('Bahrain · a café outside Fifth Fleet headquarters', 'Twenty Thousand',
  "Now there was a number. Sarah Callahan turned her phone toward Lt. Kim Junho. About 3,200 ships trapped west of the strait. About 20,000 seafarers. \"The ones I count aren't even one percent of that.\" \"The ones you count have names. Twenty thousand have no names. The bigger the number, the less people feel.\" Yesterday Asaluyeh, today Haifa. The fire was going all the way around the Gulf.",
  "\"Starting today, U.S. forces are hunting drones and fast boats over the strait. But that won't bring the ships out. What owners fear is the number on the insurance policy.\" \"Then what brings them out?\" \"A phone call. Like India did.\" \"In Tehran, the people who could take that call are fewer every day.\" The side making war counts enemies. The side trapped by it counts days.",
  'img_john_finn', 'vid_bainbridge'),
 ('Mediterranean · USS Gerald R. Ford, bound for Crete', 'Distance Shows the Whole',
  "Capt. Marcus Webb was moving away from the war. Six hundred cots lined the hangar deck. His orders said: temporary departure from the operating area. He read the evening intelligence summary. South Pars. Ras Laffan. Haifa. Kuwait. And one F-35 hit over Iran. It meant the sky of this war no longer belonged to one side.",
  "He wrote in his notebook. Our ally struck what we told them not to. Or what we approved. Which one, I learn from the news. Everyone is firing and no one has the stick. He wrote again. There are forty-five hundred people on my ship. Bringing them home whole is also the mission. For the first time, he did not turn down Sarah's request for an interview. It was her sixth.",
  'vid_carrier_sea', 'img_ford_deck'),
 ('Tehran · Imam Khomeini Hospital dormitory', 'Four Is Enough',
  "Maryam came up to the room after the night shift. Nariman was awake. The year would turn at 6:16 this evening. On the little table by the window were things her daughter had laid out alone. One apple. One candle. Two coins. And on wet cotton in a paper cup, lentils sprouted the length of a fingernail. For ten days the child had been saving spoonfuls of her lunch lentils and soaking them.",
  "\"Maman, I set the table. I couldn't do seven. It's four.\" Maryam took a long breath so as not to cry. \"Four is enough, joonam. All the most important things are here. You have sprouts.\" \"This is Baba's. When Baba comes he'll put the garlic. Baba's in charge of garlic.\" One apple, one candle, two coins, lentil sprouts in a paper cup. It was the most beautiful thing in Tehran on the twenty-first day of the war.",
  'vid_tehran_dawn', 'vid_sky_blue'),
 ('Tehran · Nowruz, the moment the year turns', 'Spring Comes on Time',
  "Spring came. Azad Moradi lit a candle. On his table was a plate of sprouted wheat he had soaked on the morning the war began. He had forgotten it. The wheat had not. On television there was no leader's face. He switched it off. In the window across the way there was a light, and in the one beside it. Candles. No one had told them to.",
  "The personal phone in her drawer rang. A Tehran number. \"Leila jan. Nowruz Mobarak. I called twenty times. On the twenty-first it went through.\" Only then did Leila cry. \"The roses lived. The cats are a little thin. I don't ask what you do over there. Only, I set a place for you at the table. Next to the apple.\" The line went dead. Now she saw those roofs not as targets but as tables.",
  'vid_azadi_dusk', 'vid_sky_clouds'),
]
PAGES = []
for i, (loc, cap, m) in enumerate(NEWS, 1):
    PAGES.append(dict(n=i, kind="news", loc=loc, text=cap, media=m))
for j, (tag, h2, p1, p2, m1, m2) in enumerate(SCENES):
    n = 6 + 2 * j
    PAGES.append(dict(n=n, kind="novel", tag=tag, h2=h2, text=p1, media=m1, alt=False))
    PAGES.append(dict(n=n + 1, kind="novel", tag=tag, h2=None, text=p2, media=m2, alt=(m1 == m2), end=(n + 1 == 21)))
PAGES[-1]['tag'] = 'Langley, Virginia · CIA Iran Operations Center'; PAGES[-1]['h2'] = 'A Place at the Table'
END_NOTE = '— End of Episode 7. Continued in Episode 8. —'
PLATFORMS = {
 'longform': (3840, 2160, list(range(1, 22)), 'wide', 'Fire at South Pars', 'Epic Fury · Episode 7', 'img_f22'),
 'longform_mobile': (2160, 3840, list(range(1, 22)), 'band', 'Fire at South Pars', 'Epic Fury · Episode 7 · Mobile', 'img_f22'),
 'x': (3840, 2160, [1, 2, 3], 'wide', "The World's Largest Gas Field Burned", 'Epic Fury · Episode 7', 'vid_bainbridge'),
 'facebook': (3840, 2160, [1, 18, 19], 'wide', 'Four Is Enough', 'Epic Fury · Episode 7', 'vid_tehran_dawn'),
 'shorts': (2160, 3840, [1, 2, 3, 4, 5], 'band', 'The Fire Went Around the Gulf', 'Epic Fury · Episode 7', 'img_john_finn'),
 'reels': (2160, 3840, [8, 9, 14, 15], 'band', 'Write Only What You Saw', 'Epic Fury · Episode 7', 'vid_dark_sky'),
 'tiktok': (2160, 3840, [1, 6, 7, 16, 17], 'band', 'Aim at the Heart', 'Epic Fury · Episode 7', 'vid_tehran_smoke'),
 'threads': (2160, 2700, [1, 10, 11, 12, 13], 'band', 'Sentences That Cross', 'Epic Fury · Episode 7', 'vid_monitors'),
 'feeds': (2160, 2700, [20, 21], 'band', 'A Place at the Table', 'Epic Fury · Episode 7', 'vid_azadi_dusk'),
}
END_TITLE = 'Continued in Episode 8'; END_SUB = 'Fiction · AI narration'; END_MEDIA = "vid_sunset_sea"
END_NARR = 'Epic Fury continues in Episode 8.'
UI = {'html_lang': 'en', 'brand_left': 'WAR NOVEL', 'l1': 'Epic Fury', 'l2': 'Night Over Hormuz', 'headline': 'Episode 7 — Fire at South Pars', 'ep_badge': 'EP 07', 'sit': 'SITUATION REPORT', 'breaking': 'FICTION BREAKING', 'ticker': 'KEY EVENTS', 'cover_top': 'EPIC FURY · NIGHT OVER HORMUZ', 'cover_kind': 'NOVEL', 'disclaimer': 'A novel inspired by real events. Characters and dialogue are invented.', 'title': 'Epic Fury: Night Over Hormuz — Episode 7: Fire at South Pars', 'rep': 'Replace', 'dele': 'Delete', 'aria': 'Play narration', 'novideo': 'Your browser does not support embedded video.', 'light': '☀ Light', 'dark': '🌙 Dark', 'fictional': 'a fictional event'}

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
UI['headline'] = _smart(UI['headline']); UI['title'] = _smart(UI['title'])
