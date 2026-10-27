import os, sys, json, requests, subprocess, time
OUT = "/home/claude/work/media"; os.makedirs(OUT, exist_ok=True)
MAN = os.path.join(OUT, "manifest.json")
man = json.load(open(MAN)) if os.path.exists(MAN) else {}
S = requests.Session(); S.headers["User-Agent"] = "EpicFuryProduction/1.0 (heewoo.kim@gmail.com)"
PX = os.environ["PEXELS_KEY"]; PB = os.environ["PIXABAY_KEY"]

COMMONS = {
 "img_map100h": 'File:2026 map of "Operation Epic Fury Timeline - First 100 Hours" used during press briefing at the Pentagon, Arlington, Virginia on 4 March (cropped).jpg',
 "img_b2_prep": "File:A B-2 Spirit stealth bomber prepares to take off during Operation Epic Fury (9573730).jpg",
 "img_b2_depart": "File:B-2 Spirit stealth bomber departs in support of Operation Epic Fury (9595923).jpg",
 "img_f15e": "File:An F-15E Strike Eagle Takes Off for Combat Flight (9582604).jpg",
 "img_iran_launch_map": "File:Iranian missile and drone launches during the 2026 Iran war.svg",
 "img_spruance": "File:USS Spruance launching Tomahawk during Operation Epic Fury.jpg",
 "img_f16_fly": "File:F-16 Fighting Falcons fly during Operation Epic Fury (9597865).jpg",
 "img_ford_deck": "File:USS Gerald R Ford (CVN 78) Conducts Flight Operations During Operation Epic Fury (9559679).jpg",
 "img_hornet": "File:F-A-18E Super Hornet Conducts Flight Operations (9591855).jpg",
 "img_tehran_smoke": "File:Attack on areas north of Tehran 1 Avash 20 esfand 1404.webp",
 "img_borujerdi8": "File:Effects of airstrike on Shahid Borujerdi Town (8).jpg",
 "img_borujerdi4": "File:Airstrike on the residential town of Shahid Boroujerdi 4 Avash.webp",
}
STOCK = {
 "vid_dark_sky": "dark storm clouds", "vid_tehran_city": "tehran", "vid_azadi": "old man walking street morning",
 "vid_sky_blue": "blue sky", "vid_control_room": "operations center screens", "vid_monitors": "earth from space satellite",
 "vid_radar": "radar display screen", "vid_phone": "phone vibrating on table dark", "vid_analyst": "woman monitors night office",
 "vid_dust": "dust smoke", "vid_tehran_smoke": "black smoke sky", "vid_azadi_dusk": "dramatic sunset sky clouds",
 "vid_sea_strait": "oil tanker ship sea", "vid_carrier_sea": "navy ship ocean", "vid_sunset_sea": "sunset ocean waves",
 "vid_seoul_night": "seoul night", "vid_sky_clouds": "clouds blue sky timelapse", "vid_tehran_dawn": "sunrise city skyline",
}

def strip(h):
    import re; return re.sub("<[^>]+>", "", h or "").strip()

def commons(key, title):
    r = S.get("https://commons.wikimedia.org/w/api.php", params=dict(action="query", titles=title, prop="imageinfo",
        iiprop="url|size|extmetadata", iiurlwidth=3840, format="json")).json()
    pg = next(iter(r["query"]["pages"].values())); ii = pg["imageinfo"][0]; md = ii["extmetadata"]
    url = ii["thumburl"] if (title.endswith(".svg") or title.endswith(".webp") or ii["width"] > 3840) else ii["url"]
    ext = ".png" if title.endswith(".svg") else ".jpg"
    raw = os.path.join(OUT, key + "_src"); dst = os.path.join(OUT, key + ext)
    open(raw, "wb").write(S.get(url).content)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, dst], check=True); os.remove(raw)
    man[key] = dict(type="image", file=os.path.basename(dst), title=title[5:], width=ii["width"], height=ii["height"],
        author=strip(md.get("Artist", {}).get("value")), license=strip(md.get("LicenseShortName", {}).get("value")),
        date=strip(md.get("DateTimeOriginal", {}).get("value")), site="Wikimedia Commons",
        page=ii["descriptionurl"], source_url=url)

def pexels(q):
    r = S.get("https://api.pexels.com/videos/search", headers={"Authorization": PX},
              params=dict(query=q, per_page=40, size="large", orientation="landscape")).json()
    best = []
    for v in r.get("videos", []):
        fs = [f for f in v["video_files"] if (f.get("width") or 0) >= 3840 and f.get("file_type") == "video/mp4"]
        if fs and 6 <= v["duration"] <= 40:
            f = min(fs, key=lambda f: f["width"])
            best.append((v, f))
    return best

def pixabay(q):
    r = S.get("https://pixabay.com/api/videos/", params=dict(key=PB, q=q, per_page=40, safesearch="true")).json()
    best = []
    for h in r.get("hits", []):
        f = h["videos"].get("large")
        if f and f.get("width", 0) >= 3840 and h["type"] != "animation" and "ai generated" not in h["tags"] and 6 <= h["duration"] <= 40:
            best.append((h, f))
    return best

def stock(key, q, pick=0):
    c = pexels(q)
    used = {m.get("source_id") for m in man.values()}
    c = [x for x in c if f"pexels-{x[0]['id']}" not in used]
    dst = os.path.join(OUT, key + ".mp4")
    if c:
        v, f = c[min(pick, len(c)-1)]
        url = f["link"]; meta = dict(site="Pexels", author=v["user"]["name"], page=v["url"], license="Pexels License (free)",
                                     source_id=f"pexels-{v['id']}", width=f["width"], height=f["height"], duration=v["duration"])
    else:
        c = pixabay(q); c = [x for x in c if f"pixabay-{x[0]['id']}" not in used]
        if not c: print("NONE", key, q); return
        h, f = c[min(pick, len(c)-1)]
        url = f["url"]; meta = dict(site="Pixabay", author=h["user"], page=h["pageURL"], license="Pixabay Content License (free)",
                                     source_id=f"pixabay-{h['id']}", width=f["width"], height=f["height"], duration=h["duration"])
    with S.get(url, stream=True) as r:
        with open(dst, "wb") as fo:
            for ch in r.iter_content(1 << 20): fo.write(ch)
    man[key] = dict(type="video", file=os.path.basename(dst), title=q, source_url=url, **meta)

keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(COMMONS) + list(STOCK)
for k in keys:
    if k in man and os.path.exists(os.path.join(OUT, man[k]["file"])) and "--force" not in sys.argv: continue
    try:
        commons(k, COMMONS[k]) if k in COMMONS else stock(k, STOCK[k])
        print("OK", k, man[k].get("width"), man[k].get("height"), man[k].get("site"), man[k].get("page"))
    except Exception as e:
        print("ERR", k, e)
    json.dump(man, open(MAN, "w"), ensure_ascii=False, indent=1)
