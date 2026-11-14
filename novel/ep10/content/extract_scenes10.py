# EP10 원고 HTML → 장면 JSON (place, time, paras[(class, text)])
import json, sys, re
from bs4 import BeautifulSoup
A = "/mnt/user-data/attachments/6c68f1a1-a772-5c01-8111-c90c6c3a4e68/"
SRC = {"ko": A + "fd36671d-epic_fury_ep10_final.html", "en": A + "5f175463-epic_fury_ep10_en.html", "jp": A + "5a68552b-epic_fury_ep10_jp.html"}
STOP = re.compile(r"(insert|summary|char-status|love|anno|next-ep|continues|bg-analysis|background|sources|cs-|ep-end|chapter-end)")
for L, f in SRC.items():
    soup = BeautifulSoup(open(f).read(), "html.parser")
    out = []; cur = None
    for el in soup.find_all(["div", "p"]):
        cls = " ".join(el.get("class") or [])
        if el.name == "div" and "scene" in (el.get("class") or []) and el.find(class_="scene-place"):
            cur = dict(place=el.find(class_="scene-place").get_text().strip().replace(" ,", ","),
                       time=el.find(class_="scene-time").get_text().strip(), paras=[]); out.append(cur); continue
        if cur is None: continue
        if el.name == "div" and STOP.search(cls) and len(out) == 7: cur = None; continue
        if el.name == "p" and el.parent.name in ("main", "div", "section", "article") and not el.find_parent(class_=re.compile("image-block|intel|flashnews|cs-card|anno|insert|summary|shareable|scene-indicator")):
            t = el.get_text().strip()
            t = re.sub(r"\s+([,.?!)」』”’])", r"\1", t); t = re.sub(r"([(「『“‘])\s+", r"\1", t); t = re.sub(r"\s{2,}", " ", t)
            if not t: continue
            c = [x for x in (el.get("class") or []) if x in ("reveal", "factual", "dialogue", "impact", "shareable")]
            cur["paras"].append([c[0] if c else "", t])
    json.dump(out, open(f"scenes_{L}.json", "w"), ensure_ascii=False, indent=1)
    print(L, len(out), [len(s["paras"]) for s in out]); print("  ", [s["place"][:40] for s in out])
    print("   last:", out[-1]["paras"][-1][1][:120])
