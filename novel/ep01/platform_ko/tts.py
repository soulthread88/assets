import os, sys, json, requests, subprocess, time
sys.path.insert(0, os.path.dirname(__file__))
from content_ko import P, C, COVERS, PLATFORMS
TC = os.environ["TYPECAST_API_KEY"]; VOICE = "tc_6296a815b958a8ed9610b189"
units = {}
for pid, d in {**P, **C}.items(): units[pid] = d["text"]
for plat, d in COVERS.items(): units["cover_" + plat] = d["narr"]
need = set()
for plat, (w, h, seq, lay) in PLATFORMS.items():
    need.add("cover_" + plat); need.update(seq)
out = {}
for k in sorted(need):
    fn = f"audio/ep01_ko_{k}.mp3"
    if not os.path.exists(fn):
        for a in range(4):
            r = requests.post("https://api.typecast.ai/v1/text-to-speech", headers={"X-API-KEY": TC},
                json={"voice_id": VOICE, "text": units[k], "model": "ssfm-v30", "language": "kor",
                      "prompt": {"emotion_preset": "normal", "emotion_intensity": 1.0},
                      "output": {"audio_format": "mp3", "audio_tempo": 1.0, "volume": 100}}, timeout=180)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("audio"):
                open(fn, "wb").write(r.content); break
            print("retry", k, r.status_code, r.text[:200]); time.sleep(5)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn]))
    out[k] = dict(file=os.path.basename(fn), dur=round(dur, 3), chars=len(units[k]), text=units[k])
    print(k, out[k]["dur"], flush=True)
json.dump(out, open("audio/durations.json", "w"), ensure_ascii=False, indent=1)
print("TOTAL chars", sum(v["chars"] for v in out.values()))
