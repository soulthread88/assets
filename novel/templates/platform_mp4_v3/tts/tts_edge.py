"""EN/JP narration — free Edge voices (EN en-US-BrianNeural, JP ja-JP-KeitaNeural, rate -5%).
Edge uses a WebSocket, so run this on a PC with normal internet (pip install edge-tts), then copy the mp3s
next to the renderer and run make_durations.py.  EF_CONTENT=content_ep02_en EF_AUDIO=./audio_en python tts_edge.py en"""
import os, sys, asyncio, importlib
import edge_tts
L = sys.argv[1]
sys.path.insert(0, os.environ.get("EF_CONTENT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content")))
K = importlib.import_module(os.environ.get("EF_CONTENT", f"content_epXX_{L}"))
VOICE = {"en": "en-US-BrianNeural", "jp": "ja-JP-KeitaNeural"}[L]
D = os.environ.get("EF_AUDIO", f"audio_{L}"); os.makedirs(D, exist_ok=True)
U = {f"p{p['n']:02d}": p["text"] for p in K.PAGES}
for k, v in K.PLATFORMS.items(): U[f"cover_{k}"] = v[4] + ("." if L == "en" else "。")
U["end"] = K.END_NARR
# TTS reads straight quotes and digits better: write numbers the way they should be spoken in the content text (e.g. "One-fifteen").
async def one(sem, k, t):
    fn = os.path.join(D, f"ep{K.EP2}_{L}_{k}.mp3")
    if os.path.exists(fn) and os.path.getsize(fn) > 1000: return
    async with sem:
        for a in range(4):
            try: await edge_tts.Communicate(t.replace("“", '"').replace("”", '"').replace("’", "'"), VOICE, rate="-5%").save(fn); return
            except Exception as e: print("retry", k, e); await asyncio.sleep(3)
async def main():
    sem = asyncio.Semaphore(4); await asyncio.gather(*[one(sem, k, t) for k, t in U.items()]); print("done", len(U))
asyncio.run(main())
