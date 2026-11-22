#!/usr/bin/env python3
"""Proofread a script with the public LanguageTool API. usage: lt_check.py <file> <en-US|ja-JP>"""
import sys, json, time, urllib.request, urllib.parse
IGNORE = {"WHITESPACE_RULE", "EN_QUOTES", "DASH_RULE", "MORFOLOGIK_RULE_EN_US_NAMES", "COMMA_PARENTHESIS_WHITESPACE"}
text = open(sys.argv[1], encoding="utf-8").read()
lines = [l for l in text.splitlines() if l and not l.startswith("===")]
chunks, cur = [], ""
for l in lines:
    if len((cur + "\n" + l).encode()) > 15000:
        chunks.append(cur); cur = l
    else:
        cur = (cur + "\n" + l) if cur else l
chunks.append(cur)
n = 0
for c in chunks:
    data = urllib.parse.urlencode({"text": c, "language": sys.argv[2], "level": "picky" if sys.argv[2].startswith("en") else "default"}).encode()
    for _ in range(3):
        try:
            d = json.loads(urllib.request.urlopen("https://api.languagetool.org/v2/check", data, timeout=60).read()); break
        except Exception as e:
            time.sleep(8)
    for m in d["matches"]:
        if m["rule"]["id"] in IGNORE:
            continue
        ctx = m["context"]; bad = ctx["text"][ctx["offset"]:ctx["offset"] + ctx["length"]]
        sug = ", ".join(r["value"] for r in m["replacements"][:3])
        print(f'[{m["rule"]["id"]}] "{bad}" -> {sug} | {m["message"][:90]} | …{ctx["text"][max(0,ctx["offset"]-30):ctx["offset"]+40]}…')
        n += 1
    time.sleep(4)
print("issues:", n)
