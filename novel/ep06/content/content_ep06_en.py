# -*- coding: utf-8 -*-
"""EPIC FURY platform MP4 — EP06 content (EN, U.S. style). Template v3: 21 pages = 5 news + 8 scenes x 2 screens.
EP06 has nine scenes: the last two screens go to scene 8 (Han Jiwon) and scene 9 (the language of war, Kang Yujin)."""
LANG = 'en'
EP_NO = "6"; EP2 = "06"
SUBTITLE = "Larijani's Morning"
DATE = 'Mar. 16, 2026'
BREAKING = ["Israeli night strike kills Ali Larijani, Supreme National Security Council secretary, and Basij commander Soleimani",
            "Trump: \"We don't need anyone's help\" — China and NATO Europe refuse warships; Japan, South Korea, Australia criticized"]
TICKER = ["Mar. 16 — China, NATO Europe refuse Hormuz military aid", "Mar. 16 — 11 Tehran apartment buildings destroyed; Dubai airport fuel tank fire",
          "Mar. 17 — Larijani, Soleimani and 300 Basij officers killed", "Mar. 17 — Elderly couple killed in Ramat Gan; Israel invades south Lebanon",
          "Mar. 17 — Trump rejects NATO help; Joe Kent resigns"]
NEWS = [
 ('Washington · Beijing · Brussels, Mar. 16',
  "On March 16 China and the European members of NATO turned down President Trump's request for military help to reopen the Strait of Hormuz. Japan, South Korea and Australia sent no warships either. The same day Iran said the strait was open to everyone except the United States and its allies. Instead of warships, the strait had a doorman.",
  'vid_lincoln6'),
 ('Tehran · Dubai · Abu Dhabi, Mar. 16',
  "That day 65 percent of the airstrikes fell on Tehran. Eleven apartment buildings collapsed, among them an eight-story block on Zarafshan Street, and Mehrabad Airport was hit. In the Gulf a drone set a fuel tank ablaze at Dubai International Airport, and fire broke out at the port of Fujairah. Near Abu Dhabi a rocket killed one person.",
  'img_tehran_mar16'),
 ('Tehran, before dawn, Mar. 17',
  "Before dawn on March 17 an Israeli night strike killed Ali Larijani, secretary of Iran's Supreme National Security Council, and Basij commander Gholamreza Soleimani. Some 300 Basij officers were reported killed with them. Larijani had been speaker of parliament and chief nuclear negotiator, and the man who announced the interim leadership council the day after the leader died.",
  'img_tehran_west'),
 ('Ramat Gan · south Lebanon · Bushehr, Mar. 17',
  "Iran answered with missiles the same day. In Ramat Gan, Israel, an elderly couple was killed on the way to a shelter, and Tel Aviv's Savidor Central station was damaged. Israel began a ground invasion of south Lebanon. A strike landed near the Bushehr nuclear plant, without damage. In Washington, counterterrorism chief Joe Kent resigned in protest of the war.",
  'img_telaviv'),
 ('Washington · Lebanon, Mar. 17',
  "On the night of March 17 President Trump wrote on Truth Social that he did not need NATO's help, and criticized Japan, South Korea and Australia. The United States, he said, needed no one's help. In Lebanon 886 people had been killed and 2,141 wounded in two weeks. UNICEF said 300 children had died in the war. The list of erased names kept growing.",
  'img_bachoura'),
]
SCENES = [
 ('Washington, D.C. · NSC Middle East office', 'The Unopened Box of Pins',
  "There was a map on the wall. It should have had flag pins in it. Brian Collins was the National Security Council's senior director for the Middle East. His job was the list of countries that would send warships to Hormuz. In two days he had made twenty-three calls. In the winter of 1991 walls like this ran out of pins. This year the box of pins sat on his desk, unopened.",
  "\"Europe's out. Tokyo, Seoul and Canberra say the same.\" He had seen it coming. An alliance is not a friendship. It is arithmetic. Those countries' tankers were trapped in the Gulf. Send warships, and those ships became targets. He put the pins in a drawer and titled his memo: Coalition status, not applicable. A war started alone has to be ended alone. The loneliest arithmetic there is.",
  'vid_phone', 'img_spruance6'),
 ('Kuwait City · Salmiya', "A City's Night",
  "The children were asleep. Fatima al-Rashid had put her three to bed and was sitting in the living room. A siren went off outside. Since the war began every sound meant something else. An engine became a missile; a door closing became an explosion. A dull thud in the distance. The windows shook. Her youngest, five, was crying. Something was frightening. That was enough.",
  "Fatima held him and looked out. In every window across the street someone stood the same way, holding a child, looking up at the sky. It was not one home's night. It was a city's. This country was on no side of this war. But there were U.S. bases on its soil. In the summer of 1990 she had been seven. She had lived to keep that summer from passing to her children.",
  'vid_dark_sky', 'vid_seoul_night'),
 ('Langley, Virginia · CIA Iran Operations Center', 'The Right-Hand List',
  "A name moved from the left-hand list on the screen to the right. Left: in office. Right: pending confirmation of removal. The name was Ali Larijani. Dr. Leila Shirazi had read him for sixteen years. A politician with a doctorate on Kant. She had never liked him. But his sentences always had arithmetic in them. With an opponent who calculates, you can bargain.",
  "\"Big one,\" Sam said. There was no joy in it. \"Sam, of the people on the right, how many ever sat at a negotiating table? On the left there's the men who shoot, and a leader who won't show his face.\" She wrote: in a war bombing cannot end, we are erasing the people who could say end it. The hard part is leaving someone to sign the paper.",
  'vid_analyst', 'vid_monitors'),
 ('Bahrain · U.S. Fifth Fleet liaison cell', 'An Answer Without an Answer',
  "On the morning board Lt. Kim Junho saw the name Larijani, a name from his academy classes, now in the presumed-dead column. Lt. Cmdr. Mark Henderson of the U.S. Navy handed him coffee. \"Hear your country's not coming.\" He said it like the weather. \"Our president'll post something soon. Korea, Japan, Australia. What'll your president say?\" \"Probably nothing.\"",
  "\"That's diplomacy. Saying nothing is saying something.\" In the summer of 1950 sixteen countries sent troops for his country. But this morning he was not sure that saying nothing was right. The three paragraphs he had sent Seoul two days ago had drawn no reply. No reply was a reply too. He went back and called out the ships' names. One had six days of water left.",
  'vid_control_room', 'vid_lincoln6'),
 ('Ramat Gan, Israel · a residential street', 'The Stairs',
  "The alarm went off. David Levy was seventy-two. A tank crewman in 1973; in 2006 a father who sent his son to the northern front. He lived on the fourth floor. Sixty-eight steps to the shelter. His knees were not what they were. On the second-floor landing he caught up with the couple from downstairs, both past eighty, the husband holding his wife's elbow. \"Go ahead, David. We'll go at our pace.\"",
  "He went ahead. For the rest of his life he would remember that sentence. The blast came before the sound. The whole stairwell lifted once and dropped. The sound left his ears. He was lying across the shelter's threshold. Alive. He looked back. The dust stood like a wall. Civilians do not choose the war. The war chooses civilians. The slowest walkers first.",
  'img_telaviv', 'vid_dust'),
 ('South Lebanon · a border observation post', 'The Storeroom Key',
  "The tracks of a Merkava tank were much lower than people think. Quiet. Ominously quiet. The quiet froze Mohammad Qasir, twenty-six, at his post. Smoke rose along the ridge. Airstrikes come down from the sky. This came across the ground. Armor, infantry, artillery. The oldest form of war. Today's order was one line. Hold your position. \"They're coming in. Tanks.\"",
  "He picked up his rifle. It was everything he had in this war. Last week his mother had left for Tyre, one of seven hundred thousand. As she left she pressed a key into his hand. The storeroom key. She called it the key to the olive grove. Was he here for Tehran or for that key? Today there was no time to ask.",
  'img_bachoura', 'vid_sky_blue'),
 ('Tehran · an alley south of Sharif University', 'Red Wednesday',
  "The fire was lit. It was the night of Chaharshanbe Suri. Soraya Tahir set up in the middle of the alley the door she had stacked six days ago. The match caught on the third try. The checkpoint had stood empty for six days. No one would come to stop the fires. Windows opened one by one. A woman with a baby, a man in an undershirt, a grandmother with a cane came down.",
  "Soraya jumped first. \"My yellow to you, your red to me!\" The next person jumped. The grandmother walked once around the fire, and it counted. An explosion to the north. Fire falling and fire lit. \"That's their fire!\" the man shouted, and jumped. People laughed. A trade kept for three thousand years. Spring does not ask permission. The fire simply lit.",
  'vid_azadi_dusk', 'vid_azadi'),
 ('Seoul · Ministry of Foreign Affairs, Africa and Middle East Bureau', "The Third Paragraph Travels",
  "First Secretary Han Jiwon watched people cross the Gwanghwamun intersection. Faces that knew nothing. On her screen was the post from Washington overnight. No need for NATO. Japan, South Korea, Australia. \"No official response. Just draft something.\" She opened another file. Three paragraphs from a navy lieutenant in Bahrain. A warship can escort a ship. It cannot bring out one already trapped.",
  "In Tehran a negotiator died. On a stairway in Ramat Gan an old couple never made it down. Tanks crossed a border; a child cried in Kuwait. In Seoul a first secretary moved a lieutenant's paragraph to the top of her own report. And millions switched off the news. War is cruelest when we get used to it. In Kang Yujin's model, there was one less person who could talk.",
  'vid_seoul_night', 'vid_sky_clouds'),
]
PAGES = []
for i, (loc, cap, m) in enumerate(NEWS, 1):
    PAGES.append(dict(n=i, kind="news", loc=loc, text=cap, media=m))
for j, (tag, h2, p1, p2, m1, m2) in enumerate(SCENES):
    n = 6 + 2 * j
    PAGES.append(dict(n=n, kind="novel", tag=tag, h2=h2, text=p1, media=m1, alt=False))
    PAGES.append(dict(n=n + 1, kind="novel", tag=tag, h2=None, text=p2, media=m2, alt=(m1 == m2), end=(n + 1 == 21)))
PAGES[-1]['tag'] = 'Nowhere · The Language of War'; PAGES[-1]['h2'] = 'Getting Used to It'
END_NOTE = '— End of Episode 6. Continued in Episode 7. —'
PLATFORMS = {
 'longform': (3840, 2160, list(range(1, 22)), 'wide', "Larijani's Morning", 'Epic Fury · Episode 6', 'img_tehran_mar16'),
 'longform_mobile': (2160, 3840, list(range(1, 22)), 'band', "Larijani's Morning", 'Epic Fury · Episode 6 · Mobile', 'img_tehran_mar16'),
 'x': (3840, 2160, [1, 2, 3], 'wide', 'The Negotiator Erased', 'Epic Fury · Episode 6', 'vid_lincoln6'),
 'facebook': (3840, 2160, [1, 8, 9], 'wide', "A City's Night", 'Epic Fury · Episode 6', 'vid_dark_sky'),
 'shorts': (2160, 3840, [1, 2, 3, 4, 5], 'band', "We Don't Need Anyone's Help", 'Epic Fury · Episode 6', 'img_spruance6'),
 'reels': (2160, 3840, [12, 13, 20, 21], 'band', 'Saying Nothing Is Saying Something', 'Epic Fury · Episode 6', 'vid_seoul_night'),
 'tiktok': (2160, 3840, [1, 14, 15, 18, 19], 'band', 'My Yellow to You, Your Red to Me', 'Epic Fury · Episode 6', 'vid_azadi_dusk'),
 'threads': (2160, 2700, [1, 6, 7, 10, 11], 'band', 'Is Anyone Left to Say End It?', 'Epic Fury · Episode 6', 'vid_monitors'),
 'feeds': (2160, 2700, [16, 17], 'band', 'The Storeroom Key', 'Epic Fury · Episode 6', 'img_bachoura'),
}
END_TITLE = 'Continued in Episode 7'; END_SUB = 'Fiction · AI narration'; END_MEDIA = "vid_sunset_sea"
END_NARR = 'Epic Fury continues in Episode 7.'
UI = {'html_lang': 'en', 'brand_left': 'WAR NOVEL', 'l1': 'Epic Fury', 'l2': 'Night Over Hormuz', 'headline': "Episode 6 — Larijani's Morning", 'ep_badge': 'EP 06', 'sit': 'SITUATION REPORT', 'breaking': 'FICTION BREAKING', 'ticker': 'KEY EVENTS', 'cover_top': 'EPIC FURY · NIGHT OVER HORMUZ', 'cover_kind': 'NOVEL', 'disclaimer': 'A novel inspired by real events. Characters and dialogue are invented.', 'title': "Epic Fury: Night Over Hormuz — Episode 6: Larijani's Morning", 'rep': 'Replace', 'dele': 'Delete', 'aria': 'Play narration', 'novideo': 'Your browser does not support embedded video.', 'light': '☀ Light', 'dark': '🌙 Dark', 'fictional': 'a fictional event'}

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
