# -*- coding: utf-8 -*-
"""EP01 KR script — every line is taken from epic_fury_ep01_final.html (abridged, not invented).
kind: cover | news | novel | end.  text = on-screen text = narration (read verbatim)."""

EP_TITLE = "제1화 · 성벽이 무너지는 날"
SERIES = "장대한 분노"
SUB = "호르무즈의 밤"
DATE = "2026. 2. 28"
DISCLAIMER = "실제 전쟁에서 착상한 소설입니다. 등장인물과 대화는 창작입니다."

# ---- longform pages (shared pool; short platforms pick from it) ----
P = {}
def page(pid, kind, label, text, media, tag=None, sub=None):
    P[pid] = dict(id=pid, kind=kind, label=label, text=text, media=media, tag=tag, sub=sub)

page("intro", "novel", "작가의 말",
     "이 소설은 2026년 2월 28일 개시된 미국과 이스라엘의 대이란 군사작전에서 착상을 얻은 픽션입니다. "
     "등장인물과 모든 대화는 작가의 창작이며, 실존 인물의 실제 언행과 무관합니다.",
     "img_map100h", tag="FICTION")

# 5 news pages (fact skeleton from the HTML timeline/flashnews)
page("n1", "news", "워싱턴 D.C. · 2월 27일 오후 3시 38분 (미 동부)",
     "2월 27일 오후 3시 38분, 미 동부 시각. 트럼프 대통령이 작전명 '장대한 분노'의 실행을 명령했다. "
     "1월과 2월, 미국은 2003년 이라크 침공 이후 최대 규모의 병력을 중동에 모아 둔 상태였다.",
     "img_b2_prep", tag="소설 속보")
page("n2", "news", "테헤란 · 2월 28일 오전 9시 45분",
     "2월 28일 오전 9시 45분, 테헤란. 미국의 '장대한 분노'와 이스라엘의 '포효하는 사자'가 동시에 시작되었다. "
     "테헤란과 쿰, 케르만샤, 이스파한, 카라지에서 폭발이 이어졌다.",
     "img_b2_depart", tag="소설 속보")
page("n3", "news", "테헤란 · 오전 10시 15분",
     "오전 10시 15분, 이스라엘 공군이 테헤란의 최고지도자 관저 단지 등 지도부를 타격했다. "
     "알리 하메네이와 군 수뇌부가 숨졌다. 이란 정부의 공식 확인은 3월 1일에야 나왔다.",
     "img_f15e", tag="소설 속보")
page("n4", "news", "이란 남부 미나브 · 오전",
     "같은 날 오전, 이란 남부 미나브의 샤자레 타이예베 여자 초등학교가 피격되었다. "
     "이란 매체는 180명이 숨졌다고 보도했다. 대부분 어린이였다.",
     "vid_dark_sky", tag="소설 속보")
page("n5", "news", "테헤란 · 낮 12시 35분",
     "낮 12시 35분, 이란은 보복 작전 '진실의 약속 4'를 개시했다. 12시 56분 바레인의 미 5함대 시설이 피격되었고, "
     "공격은 걸프 각국과 이라크 아르빌, 요르단으로 번졌다.",
     "img_iran_launch_map", tag="소설 속보")

# novel pages (scene text from the HTML, condensed)
page("s1a", "novel", "테헤란 · 아자디 광장 인근 골목 · 오전 9시 45분",
     "모든 전쟁은 누군가의 아침에서 시작되었다. 2026년 2월 28일 토요일, 오전 9시 45분. "
     "테헤란의 하늘은 파랬다. 불합리하게, 불공평하게 파랬다.",
     "vid_sky_blue", sub="장면 1 / 8")
page("s1b", "novel", "테헤란 · 아자디 광장 인근 골목",
     "아자드 모라디 교수는 아자디 광장 옆 골목에 서 있었다. 아자디. 페르시아어로 '자유'다. "
     "이 나라에서 자유는 47년 가까이 이름으로만 남았다.",
     "vid_azadi", sub="장면 1 / 8")
page("s1c", "novel", "테헤란 · 아자디 광장 인근 골목",
     "교수는 일흔두 살이었다. 어제 오후, 그의 대학원 제자 세 명이 도덕경찰에 끌려갔다. "
     "공론장을 말하던 학생들이 공론장에서 사라졌다. 그는 하늘을 올려다보았다. 오늘 하늘은 어제의 하늘이 아니다.",
     "vid_dark_sky", sub="장면 1 / 8")
page("s2a", "novel", "버지니아주 알링턴 · 펜타곤 국가군사지휘센터 · 새벽 1시 15분",
     "같은 시각, 워싱턴 D.C.는 새벽 1시 15분이었다. 포토맥 강 건너 펜타곤 지하. "
     "명령은 이미 내려와 있었다. 서명은 끝났고 결재선은 닫혔다. 이 방에 남은 일은 지켜보는 것뿐이었다.",
     "vid_control_room", sub="장면 2 / 8")
page("s2b", "novel", "펜타곤 국가군사지휘센터",
     "위성에서 본 테헤란은 평범하고 넓었다. 900만 명의 아침. 화면 위의 좌표 하나하나에 그 아침들이 겹쳐 있었다. "
     "01시 15분. 첫 탄착 신호가 화면에 떴다.",
     "vid_monitors", sub="장면 2 / 8")
page("s3a", "novel", "이란 상공 · 오전 9시 45분",
     "오전 9시 45분. 중동의 하늘이 찢어졌다. 미 해군 구축함들이 쏜 토마호크가 낮게 파고들었다. "
     "B-2 스피릿과 B-1 랜서, B-52는 요새화된 탄도미사일 시설로 향했다.",
     "img_spruance", sub="장면 3 / 8")
page("s3b", "novel", "이란 상공",
     "이스라엘 공군은 전투기 약 200대를 띄웠다. 이스라엘 역사상 가장 큰 출격이었다. "
     "오전 10시 15분, 이스라엘 공군이 테헤란의 한 관저 단지를 쳤다. 거기 누가 앉아 있었는지 세계가 알기까지 몇 시간이 더 걸렸다.",
     "img_f16_fly", sub="장면 3 / 8")
page("s3c", "novel", "알보르즈 산맥 지휘소",
     "알보르즈 산맥의 지휘소. 다리우스 세파흐반드 대령은 레이더 화면이 잡음으로 덮이는 것을 지켜보았다. "
     "지휘망은 4분 만에 무너졌다. 그의 가슴에서 전혀 예상하지 못한 감정이 솟았다. 안도감이었다.",
     "vid_radar", sub="장면 3 / 8")
page("s3d", "novel", "알보르즈 산맥 지휘소",
     "책상 위에 엎어 둔 휴대전화가 떨었다. 기도 시간 앱 바데사바였다. 화면에는 페르시아어 한 줄이 떠 있었다. "
     "도움이 도착했다. 폭탄과 문장이 같은 시각에 도착했다. 하나는 건물을 부쉈고, 하나는 복종을 흔들었다.",
     "vid_phone", sub="장면 3 / 8")
page("s4a", "novel", "동지중해 · 포드함 함교",
     "마커스 웹 함장은 26시간째 잠을 자지 못했다. 첫 출격조의 마지막 기체가 전자기 캐터펄트를 떠날 때, "
     "함교에 선 그의 두 손은 완전히 고요했다. 손이 고요할수록 안의 폭풍은 사나웠다.",
     "img_ford_deck", sub="장면 4 / 8")
page("s4b", "novel", "동지중해 · 포드함 함교",
     "바레인 5함대 기지에서는 대한민국 해군 연락장교 김준호 대위가 화면의 숫자들을 보고 있었다. "
     "그가 전해 달라고 한 말은 한 줄이었다. '우리는 역사의 증인입니다.'",
     "img_hornet", sub="장면 4 / 8")
page("s5a", "novel", "버지니아주 랭글리 · CIA 이란 작전센터",
     "레일라 시라지 박사는 19시간째 이 방에 있었다. 1988년 이란 시라즈에서 태어난 분석관. "
     "지금 그녀는 세 개의 위성 피드 화면으로, 자기가 태어난 나라의 수도가 폭격당하는 것을 보고 있었다.",
     "vid_analyst", sub="장면 5 / 8")
page("s5b", "novel", "CIA 이란 작전센터",
     "가운데 화면에 테헤란 에빈 구가 떠 있었다. 고모 페레슈테가 사는 곳. 장미 꽃잎으로 차를 끓이는 여자. "
     "지금 그 화면에 연기 기둥이 있었다. 레일라는 울지 않았다. 움직이면 떨어뜨릴까 봐, 아주 고요하게 앉아 있었다.",
     "img_tehran_smoke", sub="장면 5 / 8")
page("s6a", "novel", "테헤란 에빈 구 · 골레스탄 거리 · 오전 10시 22분",
     "200미터였다. 혁명수비대의 통신 중계소와 골레스탄 거리 5층짜리 아파트 사이의 거리. "
     "소직경폭탄 한 발이 센서 오작동으로 그만큼 흘렀다. 건물은 순서대로 무너졌다.",
     "img_borujerdi8", sub="장면 6 / 8 · 소설 속 가상 사건")
page("s6b", "novel", "테헤란 에빈 구 · 골레스탄 거리",
     "그 건물에 아이가 있었다. 이름은 나리만. 일곱 살. 앞니 사이에 빈자리가 있었다. "
     "간호사인 어머니 마리암이 맨손으로 콘크리트를 들어내고 딸을 끌어안았다. 나리만은 살아 있었다.",
     "img_borujerdi4", sub="장면 6 / 8 · 소설 속 가상 사건")
page("s6c", "novel", "테헤란 에빈 구 · 골레스탄 거리",
     "전쟁은 충성이나 죄를 보고 피해자를 고르지 않는다. 전쟁은 거리로 고른다. "
     "오차의 기하학으로. 군사 목표물과 아침 식탁 사이의 200미터로.",
     "vid_dust", sub="장면 6 / 8")
page("s7a", "novel", "테헤란 · 아자디 광장 · 오전 11시 50분",
     "아자드 교수는 광장 가장자리에서 동쪽 도심의 연기를 바라보았다. 광장 너머에서 젊은이들이 노래하고 있었다. "
     "여자들은 히잡을 쓰지 않았다. 그는 일기장에 썼다. 오늘, 우리를 47년 동안 짓눌러 온 검은 장막이 찢어졌다.",
     "vid_tehran_smoke", sub="장면 7 / 8")
page("s7b", "novel", "테헤란 · 아자디 광장",
     "지금 내가 보는 것이 해방인지 파괴인지, 나는 정말로 알 수 없다. 아마 둘 다일 것이다. "
     "성벽은 양쪽에서 무언가가 부서져야 무너진다. 그는 돌 턱에 앉아 두 손에 얼굴을 묻고 울었다.",
     "vid_azadi_dusk", sub="장면 7 / 8")
page("s8a", "novel", "동지중해 · 포드 항모 전단 · 테헤란 정오",
     "웹 함장은 해도 화면을 동쪽으로 끌었다. 호르무즈 해협. 이란 해안과 오만의 무산담 반도 사이, 21마일. "
     "평시에는 전 세계 원유의 20%가 이 틈을 지난다.",
     "vid_sea_strait", sub="장면 8 / 8")
page("s8b", "novel", "동지중해 · 포드 항모 전단",
     "\"어떤 기분이에요?\" 새라 캘러한이 낮게 물었다. "
     "\"시작은 이해하는데 끝은 이해하지 못하는 무언가를 시작한 기분.\" 웹이 말했다. \"그게 늘 사실인데도, 매번 무섭다는 것.\"",
     "img_ford_deck", sub="장면 8 / 8")
page("s8c", "novel", "동지중해 · 포드 항모 전단",
     "전쟁은 막 시작되었다. 끝은, 그것이 올 때, 아직 태어나지 않은 사람들이 쓸 것이다.",
     "vid_sunset_sea", sub="장면 8 / 8")
page("yujin", "novel", "서울 · 연구실",
     "서울. AI 연구자 강유진은 연구실 모니터 앞에서 뉴스 속보를 보고 있었다. 무언가가 시작되고 있음을 느꼈다.",
     "vid_seoul_night", sub="인물 현황")
page("love", "novel", "나리만",
     "나리만이라는 아이가 있었다. 일곱 살, 눈이 컸다. 그 애는 호르무즈 해협을 몰랐다. 그 애는 아침을 먹고 있었다. "
     "하늘은 그날도 파랬다. 잔해 위로, 연기 위로, 노래 위로. 하늘은 늘, 어떻게든, 아직도 파랬다.",
     "vid_sky_clouds")
page("teaser", "novel", "다음 화 예고 · 제2화",
     "제2화. 3월 1일, 최고지도자가 없는 첫 아침. 머리를 잘랐다. 그러나 몸은 살아 있었다. "
     "장대한 분노, 2화에서 계속됩니다.",
     "vid_tehran_dawn", sub="Chapter Two")

LONGFORM = ["intro", "n1", "n2", "n3", "n4", "n5",
            "s1a", "s1b", "s1c", "s2a", "s2b", "s3a", "s3b", "s3c", "s3d",
            "s4a", "s4b", "s5a", "s5b", "s6a", "s6b", "s6c", "s7a", "s7b",
            "s8a", "s8b", "s8c", "yujin", "love", "teaser"]


# ---- extension pages (longform must exceed 8 minutes; all lines from the HTML) ----
page("n6", "news", "이란 전역 · 오전",
     "이란의 기도 시간 앱 바데사바가 해킹되었다. '도움이 도착했다'는 알림이 일제히 발송되었고, "
     "이란 방송과 기반시설에도 동시에 사이버 공격이 이어졌다.",
     "vid_radar", tag="소설 속보")
page("n7", "news", "개전 첫날 · 집계",
     "이란 적신월사는 개전 첫날 사망자가 200명을 넘었다고 밝혔다. "
     "이스라엘군은 첫 24시간 동안 500곳의 표적에 1,200발 이상의 폭탄을 썼다고 했다.",
     "img_map100h", tag="소설 속보")
page("intel", "novel", "NSA · CENTCOM 감청 · 오전 10시 47분",
     "가상 감청 문서. 반다르 아바스 기지 송신. 지휘관 응답 없음. 독자 판단으로 고속정 귀환 개시. "
     "평가. 혁명수비대 해군은 지휘 공백 상태. 호르무즈 해협의 고속정 전력은 온존.",
     "vid_control_room", tag="FICTION · 가상 문서")
page("s1d", "novel", "테헤란 · 아자디 광장",
     "그는 광장을 바라보았다. 팔레비 왕이 자기를 위해 세운 하얀 아치형 탑, 아자디 타워. "
     "혁명은 그 탑을 살려 두었다. 왕이 가고 성직자가 와도 탑은 서 있었다.",
     "vid_sky_clouds", sub="장면 1 / 8")
page("s3e", "novel", "알보르즈 산맥 지휘소",
     "열아홉 살 혁명수비대 병사가 텅 빈 하늘에 쏘던 소총을 멈추고 전화기를 내려다보았다. "
     "눈물이 얼굴을 타고 흘렀다. \"이건 전쟁이 아니야. 이건 다른 무언가야.\"",
     "vid_phone", sub="장면 3 / 8")
page("s4c", "novel", "동지중해 · 포드함 함교",
     "AP 통신 전쟁 특파원 새라 캘러한이 격벽에 기대 카메라를 들고 있었다. "
     "모술 함락과 마리우폴 포위전을 취재한 서른다섯 살 기자. 그녀는 웹을 보고 있었다.",
     "img_hornet", sub="장면 4 / 8")
page("s4d", "novel", "동지중해 · 포드함 함교",
     "\"그 장교에게 전해 주시오.\" 웹이 말했다. \"우리가 이것을 제대로 해내기를 바란다고.\" "
     "그의 옆에서 새라 캘러한의 셔터가 조용히 울렸다.",
     "vid_carrier_sea", sub="장면 4 / 8")
page("s5c", "novel", "CIA 이란 작전센터",
     "레일라는 생각했다. 나는 보고서를 썼다. 나는 타격 모델을 만들었다. "
     "그녀는 생각했다. 고모는 장미 꽃잎으로 차를 끓인다.",
     "vid_monitors", sub="장면 5 / 8")
page("s5d", "novel", "CIA 이란 작전센터",
     "\"시라지, IRGC 대응 시간 분석 좀 봐 줄 수 있어?\" \"네. 1분만요.\" "
     "그 1분 동안 그녀는 소리 없이 말했다. 미안해요. 나는 이것이 필요하다고 믿어요. 정말 미안해요.",
     "vid_analyst", sub="장면 5 / 8")
page("s8d", "novel", "동지중해 · 포드 항모 전단",
     "갑판 아래, 군종 목사는 스물세 명의 수병과 조용히 기도하고 있었다. "
     "빨리 끝나기를. 보이는 것만큼 나쁘지는 않기를.",
     "vid_sky_clouds", sub="장면 8 / 8")
page("history", "novel", "역사 메모 · 호르무즈 해협",
     "호르무즈 해협은 페르시아 만과 오만 만을 잇는다. 2월 28일 전쟁이 시작되자 해협을 지나는 배는 빠르게 줄었고, "
     "3월 1일에서 2일 사이 통항은 사실상 멈췄다.",
     "vid_sea_strait", tag="역사 메모")

LONGFORM = ["intro", "n1", "n2", "n3", "n4", "n5", "n6", "n7", "intel",
            "s1a", "s1b", "s1c", "s1d", "s2a", "s2b", "s3a", "s3b", "s3c", "s3d", "s3e",
            "s4a", "s4c", "s4b", "s4d", "s5a", "s5b", "s5c", "s5d", "s6a", "s6b", "s6c", "s7a", "s7b",
            "s8a", "s8b", "s8d", "s8c", "yujin", "love", "history", "teaser"]

# ---- short-form clips (sentences from the HTML; each platform gets its own hook/cover/CTA) ----
C = {}
def clip(cid, label, text, media, sub=None):
    C[cid] = dict(id=cid, kind="novel", label=label, text=text, media=media, sub=sub)

clip("h_sky", "테헤란 · 2026년 2월 28일 오전 9시 45분",
     "2026년 2월 28일 오전 9시 45분. 중동의 하늘이 찢어졌다.", "img_b2_depart")
clip("h_two", "테헤란 · 오전 9시 45분",
     "미국의 '장대한 분노'와 이스라엘의 '포효하는 사자'. 두 작전이 동시에 시작되었다.", "img_spruance")
clip("h_1015", "테헤란 · 오전 10시 15분",
     "오전 10시 15분, 테헤란의 최고지도자 관저 단지가 공습을 받았다. 이란 정부의 공식 확인은 3월 1일에 나왔다.", "img_f15e")
clip("c_azad", "테헤란 · 아자디 광장",
     "아자디 광장 옆 골목. 일흔두 살 철학 교수 아자드는 하늘을 올려다보았다. 오늘 하늘은 어제의 하늘이 아니다.", "vid_azadi")
clip("c_darius", "알보르즈 산맥 지휘소",
     "지휘망은 4분 만에 무너졌다. 휴대전화에 페르시아어 한 줄이 떴다. 도움이 도착했다.", "vid_phone")
clip("c_webb", "동지중해 · 포드함",
     "포드함 함교. 웹 함장의 두 손은 고요했다. 손이 고요할수록 안의 폭풍은 사나웠다.", "img_ford_deck")
clip("c_leila", "랭글리 · CIA 이란 작전센터",
     "랭글리의 분석관 레일라는 자기가 태어난 나라의 수도가 폭격당하는 것을 보고 있었다.", "vid_analyst")
clip("c_200m", "테헤란 에빈 구 · 소설 속 가상 사건",
     "200미터. 폭탄 한 발이 그만큼 흘렀다. 그 건물에 일곱 살 나리만이 있었다.", "img_borujerdi8")
clip("c_mom", "테헤란 에빈 구",
     "어머니가 맨손으로 콘크리트를 들어냈다. 나리만은 살아 있었다.", "img_borujerdi4")
clip("c_diary", "테헤란 · 아자디 광장",
     "해방인지 파괴인지, 나는 정말로 알 수 없다. 아마 둘 다일 것이다.", "vid_azadi_dusk")
clip("c_begin", "동지중해 · 포드 항모 전단",
     "전쟁은 막 시작되었다. 끝은 아직 태어나지 않은 사람들이 쓸 것이다.", "vid_sunset_sea")
clip("c_next", "제2화 예고",
     "장대한 분노, 제2화에서 계속됩니다.", "vid_tehran_dawn")
# CTAs (one per platform)
clip("cta_longform", "구독", "다음 화가 올라오면 알려 드릴게요.", "vid_tehran_dawn")
clip("cta_x", "1화 전체", "1화 전체 영상은 프로필 링크에서 볼 수 있습니다.", "vid_tehran_dawn")
clip("cta_fb", "1화 전체", "1화 전체 영상은 페이지에서 이어집니다.", "vid_tehran_dawn")
clip("cta_shorts", "롱폼", "전체 이야기는 롱폼 영상에서 이어집니다.", "vid_tehran_dawn")
clip("cta_reels", "저장", "저장해 두고 2화에서 만나요.", "vid_tehran_dawn")
clip("cta_tiktok", "팔로우", "팔로우하고 2화를 기다려 주세요.", "vid_tehran_dawn")
clip("cta_threads", "블로그", "1화 전문은 블로그에서 읽을 수 있습니다.", "vid_tehran_dawn")
clip("cta_feeds", "프로필 링크", "1화 전문은 프로필 링크에서.", "vid_tehran_dawn")

# Covers (thumbnail = first frame; title and line vary by platform)
COVERS = {
 "longform": dict(title="성벽이 무너지는 날", line="장대한 분노 EP01 · 호르무즈의 밤", media="img_ford_deck",
                  narr="장대한 분노, 호르무즈의 밤. 제1화, 성벽이 무너지는 날."),
 "x":        dict(title="오전 9시 45분, 하늘이 찢어졌다", line="장대한 분노 EP01", media="img_b2_depart",
                  narr="장대한 분노 제1화."),
 "facebook": dict(title="같은 아침, 다섯 개의 시선", line="장대한 분노 EP01 · 성벽이 무너지는 날", media="vid_sky_blue",
                  narr="장대한 분노 제1화, 성벽이 무너지는 날."),
 "shorts":   dict(title="작전명, 장대한 분노", line="EP01 소설 속보 1분", media="img_spruance",
                  narr="작전명, 장대한 분노."),
 "reels":    dict(title="200미터의 오차", line="장대한 분노 EP01", media="img_borujerdi8",
                  narr="200미터의 오차."),
 "tiktok":   dict(title="도움이 도착했다", line="장대한 분노 EP01", media="vid_phone",
                  narr="도움이 도착했다."),
 "threads":  dict(title="해방인가, 파괴인가", line="장대한 분노 EP01", media="vid_azadi",
                  narr="해방인가, 파괴인가."),
 "feeds":    dict(title="검은 장막이 찢긴 날", line="장대한 분노 EP01", media="vid_azadi_dusk",
                  narr="검은 장막이 찢긴 날."),
}

PLATFORMS = {
 # name: (W, H, sequence, layout)
 "longform": (3840, 2160, LONGFORM + ["cta_longform"], "wide"),
 "x":        (3840, 2160, ["n2", "n3", "n4", "n5", "s6b", "s7b", "c_begin", "c_next", "cta_x"], "wide"),
 "facebook": (3840, 2160, ["h_sky", "h_two", "h_1015", "c_azad", "c_darius", "c_webb", "c_leila",
                           "c_200m", "c_mom", "c_diary", "c_begin", "c_next", "cta_fb"], "wide"),
 "shorts":   (2160, 3840, ["h_sky", "h_two", "h_1015", "c_azad", "c_darius", "c_webb", "c_leila",
                           "c_200m", "c_mom", "c_diary", "c_next", "cta_shorts"], "tall"),
 "reels":    (2160, 3840, ["h_sky", "h_1015", "c_azad", "c_webb", "c_200m", "c_mom", "c_diary", "c_next", "cta_reels"], "tall"),
 "tiktok":   (2160, 3840, ["h_sky", "h_two", "c_darius", "c_leila", "c_200m", "c_mom", "c_diary", "c_begin", "c_next", "cta_tiktok"], "tall"),
 "threads":  (2160, 2700, ["h_sky", "c_azad", "c_darius", "c_200m", "c_mom", "c_diary", "c_next", "cta_threads"], "feed"),
 "feeds":    (2160, 2700, ["h_sky", "h_two", "c_200m", "c_mom", "c_next", "cta_feeds"], "feed"),
}
