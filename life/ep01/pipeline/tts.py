#!/usr/bin/env python3
"""lifestory TTS stage: script.txt -> per-paragraph Typecast audio -> narration.mp3 + timeline.json + .srt
usage: tts.py <script.txt> <outdir> <lang: ko|en|jp>
env: TYPECAST_API_KEY
"""
import os, sys, re, json, hashlib, subprocess, time, concurrent.futures as cf, urllib.request

VOICES = {  # Typecast ssfm-v30
    "ko": ("tc_6296a815b958a8ed9610b189", "kor"),  # 인화 Inhwa
    "en": ("tc_6af54d6a6b24a08feffb40b4", "eng"),  # Ozzie (Brian-like audiobook narrator)
    "jp": ("tc_640997d2c535f40558c0722c", "jpn"),  # Hideo Watanabe
}
EMO = {"hook": "normal", "intro": "happy", "goguma": "normal", "turning": "toneup",
       "saida": "toneup", "ending": "happy"}
SAD_BG = {"rain_window", "rain_street"}
PARA_GAP, SCENE_GAP = 0.45, 0.9
TEMPO = float(os.environ.get("TEMPO", "1.0"))  # <1 = slower, senior-friendly


def parse(path):
    scenes, cur = [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        m = re.match(r"^=== (\w+) \| (.+?) \| stage:(\w+) \| bg:(\w+) ===$", line)
        if m:
            cur = dict(id=m[1], title=m[2], stage=m[3], bg=m[4], paras=[])
            scenes.append(cur)
        elif line and cur is not None:
            cur["paras"].append(line)
    return scenes


def synth(text, lang, emo, cache):
    vid, code = VOICES[lang]
    key = hashlib.sha1(f"{vid}|{emo}|{text}".encode()).hexdigest()[:16]
    out = os.path.join(cache, key + ".mp3")
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return out
    body = json.dumps({"voice_id": vid, "text": text, "model": "ssfm-v30", "language": code,
                       "prompt": {"emotion_type": "preset", "emotion_preset": emo, "emotion_intensity": 1.0},
                       "output": {"audio_format": "mp3"}}).encode()
    for attempt in range(5):
        try:
            req = urllib.request.Request("https://api.typecast.ai/v1/text-to-speech", data=body, method="POST",
                                         headers={"X-API-KEY": os.environ["TYPECAST_API_KEY"],
                                                  "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            if len(data) > 1000:
                open(out + ".part", "wb").write(data)
                os.replace(out + ".part", out)
                return out
        except Exception as e:
            print("retry", attempt, str(e)[:120], file=sys.stderr)
            time.sleep(3 + attempt * 4)
    raise RuntimeError("TTS failed: " + text[:40])


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", f]).decode().strip())


def split_sentences(p, lang):
    if lang == "jp":
        parts = re.split(r"(?<=[。！？」])", p)
    else:
        parts = re.split(r"(?<=[.!?\"”])\s+", p)
    return [s.strip() for s in parts if s.strip()]


def fmt(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def main(script, outdir, lang):
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    cache = os.path.join(outdir, "cache")
    os.makedirs(cache, exist_ok=True)
    scenes = parse(script)
    jobs = []
    for s in scenes:
        emo = "sad" if s["bg"] in SAD_BG else EMO.get(s["stage"], "normal")
        for i, p in enumerate(s["paras"]):
            jobs.append((s["id"], i, p, emo))
    with cf.ThreadPoolExecutor(4) as ex:
        files = list(ex.map(lambda j: synth(j[2], lang, j[3], cache), jobs))
    # build timeline + concat list (wav, 44.1k mono)
    sil = {g: os.path.join(cache, f"sil_{g}.wav") for g in (PARA_GAP, SCENE_GAP)}
    for g, f in sil.items():
        if not os.path.exists(f):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                            "-t", str(g), f], check=True)
    t, timeline, lst, k = 0.4, [], [], 0
    lead = os.path.join(cache, "lead.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.4", lead], check=True)
    lst.append(lead)
    srt, n = [], 1
    for s in scenes:
        sc = dict(id=s["id"], title=s["title"], stage=s["stage"], bg=s["bg"], start=t, paras=[])
        for i, p in enumerate(s["paras"]):
            f = files[k]; k += 1
            wav = f[:-4] + f"_t{TEMPO}.wav"
            if not os.path.exists(wav):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-af", f"atempo={TEMPO}", "-ar", "44100", "-ac", "1", wav], check=True)
            d = dur(wav)
            sc["paras"].append(dict(text=p, start=t, end=t + d))
            sents = split_sentences(p, lang)
            tot = sum(len(x) for x in sents) or 1
            st = t
            for x in sents:
                e = st + d * len(x) / tot
                srt.append(f"{n}\n{fmt(st)} --> {fmt(e)}\n{x}\n"); n += 1
                st = e
            lst.append(wav); t += d
            gap = PARA_GAP if i < len(s["paras"]) - 1 else SCENE_GAP
            lst.append(sil[gap]); t += gap
        sc["end"] = t
        timeline.append(sc)
    with open(os.path.join(cache, "concat.txt"), "w") as fh:
        for f in lst:
            fh.write(f"file '{f}'\n")
    out = os.path.join(outdir, "narration.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(cache, "concat.txt"),
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "2", "-b:a", "192k", out], check=True)
    json.dump(dict(lang=lang, duration=t, scenes=timeline), open(os.path.join(outdir, "timeline.json"), "w"),
              ensure_ascii=False, indent=1)
    open(os.path.join(outdir, "narration.srt"), "w", encoding="utf-8").write("\n".join(srt))
    print(f"{script}: {len(jobs)} paras, {t/60:.1f} min -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
