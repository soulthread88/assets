#!/usr/bin/env python3
"""lifestory stock stage: bright, copyright-free 4K photos (Pexels) + 4K video clips (Pexels, Pixabay fallback).
usage: stock.py <outdir>   env: PEXELS_API_KEY, PIXABAY_API_KEY
Writes <outdir>/manifest.json with source/author/license per file."""
import os, sys, json, urllib.request, urllib.parse

Q = {  # bg key -> bright search query
    "wedding_ring": "wedding rings bright", "sunrise_city": "sunrise city bright", "rain_window": "rain window soft light",
    "morning_light": "morning sunlight kitchen", "notebook_desk": "notebook desk bright", "korean_restaurant": "korean food table",
    "paper_document": "document paper desk bright", "dark_window_light": "window light curtain bright",
    "night_street": "evening street lights", "bakery_morning": "bakery bread shop bright", "city_cafe": "bright cafe interior",
    "wood_workshop": "woodworking workshop", "rain_street": "rain umbrella street", "office_document": "signing contract office",
    "night_city_lights": "city lights evening", "morning_window": "morning window sunlight", "family_dining": "family dinner table",
    "bright_living_room": "bright living room", "sunlight_hall": "sunlight interior hall", "wedding_garden": "outdoor wedding garden",
    "bakery_sunlight": "bakery sunlight bread", "sunset_sky": "golden sunset sky",
}
VIDEO_KEYS = ["wedding_ring", "wood_workshop", "bakery_morning", "morning_light", "rain_window", "wedding_garden",
              "korean_restaurant", "sunset_sky"]
UA = {"User-Agent": "lifestory-pipeline/1.0"}


def get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def dl(url, out):
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(out + ".part", "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    os.replace(out + ".part", out)


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    pk = {"Authorization": os.environ["PEXELS_API_KEY"]}
    man = {}
    for key, q in Q.items():
        for orient in ("landscape", "portrait"):
            fn = f"{outdir}/{key}_{orient}.jpg"
            try:
                d = get("https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
                    {"query": q, "orientation": orient, "per_page": 8, "size": "large"}), pk)
                ph = max(d["photos"][:8], key=lambda p: (p["width"] * p["height"] >= 3840 * 2160, -abs(p.get("avg_color") and 0 or 0)))
                # prefer brightest-looking: pexels gives avg_color hex; pick highest luminance among large ones
                cands = [p for p in d["photos"] if max(p["width"], p["height"]) >= 3840] or d["photos"]
                lum = lambda p: sum(int(p["avg_color"][i:i + 2], 16) * w for i, w in ((1, .299), (3, .587), (5, .114))) if p.get("avg_color") else 128
                ph = max(cands, key=lum)
                dl(ph["src"]["original"], fn)
                man[os.path.basename(fn)] = dict(source="Pexels", url=ph["url"], author=ph["photographer"],
                                                 license="Pexels License (free to use)", w=ph["width"], h=ph["height"])
                print("photo", fn, ph["width"], ph["height"])
            except Exception as e:
                print("photo fail", key, orient, e)
    for key in VIDEO_KEYS:
        for orient in ("landscape", "portrait"):
            fn = f"{outdir}/{key}_{orient}.mp4"
            try:
                d = get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
                    {"query": Q[key], "orientation": orient, "per_page": 15, "size": "large"}), pk)
                best = None
                for v in d["videos"]:
                    if not 6 <= v["duration"] <= 40:
                        continue
                    for f in v["video_files"]:
                        if f.get("width") and max(f["width"], f["height"]) >= 3840 and f["file_type"] == "video/mp4":
                            if (orient == "landscape") == (f["width"] > f["height"]):
                                best = best or (v, f)
                if not best:
                    print("no 4k video", key, orient); continue
                v, f = best
                dl(f["link"], fn)
                man[os.path.basename(fn)] = dict(source="Pexels", url=v["url"], author=v["user"]["name"],
                                                 license="Pexels License (free to use)", w=f["width"], h=f["height"],
                                                 duration=v["duration"])
                print("video", fn, f["width"], f["height"], v["duration"])
            except Exception as e:
                print("video fail", key, orient, e)
    json.dump(man, open(f"{outdir}/manifest.json", "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1])
