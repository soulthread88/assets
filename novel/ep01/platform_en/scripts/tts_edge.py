"""Edge TTS narration for EN (en-US-BrianNeural) / JP (ja-JP-KeitaNeural). Usage: tts_edge.py en|jp [rate]"""
import os, sys, json, asyncio, subprocess, importlib
sys.path.insert(0, os.path.dirname(__file__))
import edge_tts
L = sys.argv[1]; RATE = sys.argv[2] if len(sys.argv) > 2 else "-5%"
K = importlib.import_module("content_" + L)
VOICE = {"en": "en-US-BrianNeural", "jp": "ja-JP-KeitaNeural"}[L]
D = f"audio_{L}"; os.makedirs(D, exist_ok=True)
U = {f"p{p['n']:02d}": p["text"] for p in K.PAGES}
for k, v in K.PLATFORMS.items(): U[f"cover_{k}"] = v[4] + ("." if L == "en" else "。")
U["end"] = K.END_NARR
async def one(k, t):
    fn = f"{D}/ep01_{L}_{k}.mp3"
    if not os.path.exists(fn):
        for a in range(4):
            try:
                await edge_tts.Communicate(t, VOICE, rate=RATE).save(fn); break
            except Exception as e: print("retry", k, e); await asyncio.sleep(3)
    return k, fn
async def main():
    res = await asyncio.gather(*[one(k, t) for k, t in U.items()])
    out = {}
    for k, fn in res:
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn]))
        out[k] = dict(file=os.path.basename(fn), dur=round(d, 3), text=U[k])
    json.dump(out, open(f"{D}/durations.json", "w"), ensure_ascii=False, indent=1)
    tot = sum(out[f"p{n:02d}"]["dur"] + 1.7 for n in range(1, 22)) + out["cover_longform"]["dur"] + 1.5 + out["end"]["dur"] + 1.5
    print(L, VOICE, RATE, "longform est", round(tot, 1), "s")
asyncio.run(main())
