"""밝은 4K 움직이는 영상 후보 찾기 (Pexels 우선, Pixabay 보조). 키는 환경변수 PEXELS_KEY, PIXABAY_KEY."""
import os, sys, json, io, urllib.request, urllib.parse
from PIL import Image, ImageStat
PK = os.environ["PEXELS_KEY"]; XK = os.environ["PIXABAY_KEY"]
def get(u, h=None):
    return urllib.request.urlopen(urllib.request.Request(u, headers=h or {"User-Agent": "EpicFuryMediaBot/1.0"}), timeout=40).read()
def lum(url):
    try:
        im = Image.open(io.BytesIO(get(url))).convert("L"); return ImageStat.Stat(im).mean[0]
    except Exception: return 0
def pexels(q, n=12):
    d = json.loads(get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(dict(query=q, per_page=n, size="large", orientation="landscape")), {"Authorization": PK, "User-Agent": "EpicFuryMediaBot/1.0"}))
    out = []
    for v in d.get("videos", []):
        fs = sorted([f for f in v["video_files"] if (f.get("width") or 0) >= 3840 and (f.get("height") or 0) >= 2160], key=lambda f: f["width"])
        if not fs or v["duration"] < 7: continue
        out.append(dict(site="Pexels", id=v["id"], page=v["url"], author=v["user"]["name"], license="Pexels License (free)", w=fs[0]["width"], h=fs[0]["height"],
                        dur=v["duration"], file=fs[0]["link"], thumb=v["image"], title=v["url"].rstrip("/").split("/")[-1].rsplit("-", 1)[0].replace("-", " "), query=q))
    return out
def pixabay(q, n=12):
    d = json.loads(get("https://pixabay.com/api/videos/?" + urllib.parse.urlencode(dict(key=XK, q=q, per_page=n, safesearch="true"))))
    out = []
    for h in d.get("hits", []):
        L = h["videos"].get("large", {})
        if (L.get("width") or 0) < 3840 or h["duration"] < 7: continue
        out.append(dict(site="Pixabay", id=h["id"], page=h["pageURL"], author=h["user"], license="Pixabay Content License (free)", w=L["width"], h=L["height"],
                        dur=h["duration"], file=L["url"], thumb=L.get("thumbnail") or h["videos"]["medium"].get("thumbnail"), title=h["tags"], query=q))
    return out
if __name__ == "__main__":
    Q = json.load(open(sys.argv[1])); res = {}
    for slot, qs in Q.items():
        cands = []
        for q in qs:
            try: cands += pexels(q)
            except Exception as e: print("pexels err", q, e)
            if len(cands) < 4:
                try: cands += pixabay(q)
                except Exception as e: print("pixabay err", q, e)
        for c in cands[:10]: c["L"] = round(lum(c["thumb"]))
        res[slot] = sorted(cands[:10], key=lambda c: -c["L"])
        print(slot, [(c["site"][:2], c["id"], c["L"]) for c in res[slot][:5]], flush=True)
    json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
