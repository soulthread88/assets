# Download EP01 outputs from GitHub (soulthread88) into this 100126 folder. Re-runnable.
import json, os, sys, urllib.request
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ITEMS = json.loads(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].startswith("[") else json.load(open(sys.argv[1], encoding="utf-8"))
ok = fail = 0
for url, rel in ITEMS:
    dst = os.path.join(BASE, *rel.split("/")); os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dst + ".part"); os.replace(dst + ".part", dst); ok += 1
    except Exception as e:
        fail += 1; print("FAIL", rel, e)
print("ok", ok, "fail", fail)
