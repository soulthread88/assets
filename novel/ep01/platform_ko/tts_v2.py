import os, sys, json, requests, subprocess, time
sys.path.insert(0, os.path.dirname(__file__)); import content_v2 as K
TC = os.environ["TYPECAST_API_KEY"]; VOICE = "tc_6296a815b958a8ed9610b189"
U = {f"p{p['n']:02d}": p["text"] for p in K.PAGES}
for k, v in K.PLATFORMS.items(): U[f"cover_{k}"] = f"{v[4]}."
U["end"] = K.END_NARR
out = {}
for k, t in U.items():
    fn = f"audio2/ep01_ko_{k}.mp3"
    if not os.path.exists(fn):
        for a in range(4):
            r = requests.post("https://api.typecast.ai/v1/text-to-speech", headers={"X-API-KEY": TC}, timeout=180,
                json={"voice_id": VOICE, "text": t, "model": "ssfm-v30", "language": "kor",
                      "prompt": {"emotion_preset": "normal", "emotion_intensity": 1.0}, "output": {"audio_format": "mp3"}})
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("audio"): open(fn, "wb").write(r.content); break
            print("retry", k, r.status_code, r.text[:150]); time.sleep(5)
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn]))
    out[k] = dict(file=os.path.basename(fn), dur=round(d, 3), text=t)
json.dump(out, open("audio2/durations.json", "w"), ensure_ascii=False, indent=1)
tot = sum(out[f"p{n:02d}"]["dur"] + 1.7 for n in range(1, 22)) + out["cover_longform"]["dur"] + 1.5 + out["end"]["dur"] + 1.5
print("chars", sum(len(t) for t in U.values()), "longform est", round(tot, 1))
