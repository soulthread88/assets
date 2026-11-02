"""Write durations.json for a narration folder (needed by render_v3). EF_CONTENT=... EF_AUDIO=./audio_en python3 make_durations.py en"""
import os, sys, json, subprocess, importlib
L = sys.argv[1]
sys.path.insert(0, os.environ.get("EF_CONTENT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")))
K = importlib.import_module(os.environ.get("EF_CONTENT", f"content_epXX_{L}"))
D = os.environ.get("EF_AUDIO", f"audio_{L}")
U = {f"p{p['n']:02d}": p["text"] for p in K.PAGES}
for k, v in K.PLATFORMS.items(): U[f"cover_{k}"] = v[4]
U["end"] = K.END_NARR
out = {}
for k, t in U.items():
    fn = os.path.join(D, f"ep{K.EP2}_{L}_{k}.mp3")
    if not os.path.exists(fn) and k.startswith("cover_"): fn = os.path.join(D, f"ep{K.EP2}_{L}_cover_longform.mp3")
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn]))
    out[k] = dict(file=os.path.basename(fn), dur=round(d, 3), text=t)
json.dump(out, open(os.path.join(D, "durations.json"), "w"), ensure_ascii=False, indent=1)
tot = sum(out[f"p{n:02d}"]["dur"] + 1.7 for n in range(1, 22)) + out["cover_longform"]["dur"] + out["end"]["dur"] + 3
print("ok", len(out), "longform estimate", round(tot), "s (must be >= 480)")
