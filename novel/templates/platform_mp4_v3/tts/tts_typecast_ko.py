"""KO narration — Typecast 인화 (ssfm-v30). Key from env TYPECAST_API_KEY (never write it into files).
EF_CONTENT=content_ep02_ko EF_AUDIO=./audio_ko python3 tts_typecast_ko.py"""
import os, sys, json, time, subprocess, importlib, requests
sys.path.insert(0, os.environ.get("EF_CONTENT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")))
K = importlib.import_module(os.environ.get("EF_CONTENT", "content_epXX_ko"))
TC = os.environ["TYPECAST_API_KEY"]; VOICE = "tc_6296a815b958a8ed9610b189"
D = os.environ.get("EF_AUDIO", "audio_ko"); os.makedirs(D, exist_ok=True)
U = {f"p{p['n']:02d}": p["text"] for p in K.PAGES}
for k, v in K.PLATFORMS.items(): U[f"cover_{k}"] = f"{v[4]}."
U["end"] = K.END_NARR
out = {}
for k, t in U.items():
    fn = f"{D}/ep{K.EP2}_ko_{k}.mp3"
    if not os.path.exists(fn):
        for a in range(4):
            r = requests.post("https://api.typecast.ai/v1/text-to-speech", headers={"X-API-KEY": TC}, timeout=180,
                json={"voice_id": VOICE, "text": t, "model": "ssfm-v30", "language": "kor",
                      "prompt": {"emotion_preset": "normal", "emotion_intensity": 1.0}, "output": {"audio_format": "mp3"}})
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("audio"): open(fn, "wb").write(r.content); break
            print("retry", k, r.status_code, r.text[:150]); time.sleep(5)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn]))
    out[k] = dict(file=os.path.basename(fn), dur=round(d, 3), text=t)
json.dump(out, open(f"{D}/durations.json", "w"), ensure_ascii=False, indent=1)
tot = sum(out[f"p{n:02d}"]["dur"] + 1.7 for n in range(1, 22)) + out["cover_longform"]["dur"] + out["end"]["dur"] + 3
print("longform estimate", round(tot), "s (must be >= 480)")
