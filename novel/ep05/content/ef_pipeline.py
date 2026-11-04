#!/usr/bin/env python3
"""EPIC FURY platform MP4 pipeline (cloud-worker stages). Same format as EP01/EP02 final (template v3 renderer).

  python3 ef_pipeline.py ingest   EP SRC_DIR      # Commons downloads (from the PC n8n 'media' stage) -> media_epNN + manifest.json
  python3 ef_pipeline.py audio    EP SRC_DIR      # copy Edge EN/JP mp3s (from the PC n8n 'tts' stage) into audio/en, audio/jp
  python3 ef_pipeline.py tts-ko   EP              # Typecast 인화 (env TYPECAST_API_KEY; never stored)
  python3 ef_pipeline.py durations EP             # durations.json for ko/en/jp (renderer input)
  python3 ef_pipeline.py render   EP [BUDGET_MIN] # render pending MP4s (resumable); stops before a job would pass the budget
  python3 ef_pipeline.py upload   EP LANG...      # GitHub videos/assets (+LFS >95MB), audio
  python3 ef_pipeline.py manifest EP              # sync manifest (url|name|md5) for the PC n8n 'sync' stage, pushed to assets
  python3 ef_pipeline.py status   EP
Work dir: /home/claude/work/epNN  (content_epNN_{ko,en,jp}.py written by the LLM step)."""
import os, sys, json, glob, shutil, subprocess, hashlib, time, re, importlib
ROOT = "/home/claude/work"; KIT = f"{ROOT}/tplkit"; BASE_MEDIA = f"{ROOT}/media"
PLATS = ["x", "facebook", "shorts", "reels", "tiktok", "threads", "feeds", "longform", "longform_mobile"]
LANGS = ["en", "jp", "ko"]
GIT = ["-c", "user.name=soulthread88", "-c", "user.email=heewoo.kim@gmail.com"]
TRAILER = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PY7NmpQMmmge1DdA9jzQEc"
def sh(*a, **k): return subprocess.run(a, check=True, **k)
def out(*a, **k): return subprocess.check_output(a, **k).decode()
def dirs(ep):
    E = "%02d" % int(ep); W = f"{ROOT}/ep{E}"
    return E, W, f"{ROOT}/media_ep{E}"
def strip(h): return re.sub("<[^>]+>", "", h or "").strip()

def ingest(ep, src):
    E, W, M = dirs(ep); os.makedirs(M, exist_ok=True)
    man = json.load(open(f"{BASE_MEDIA}/manifest.json"))
    prev = f"{ROOT}/media_ep%02d/manifest.json" % (int(ep) - 1)
    if os.path.exists(prev): man.update(json.load(open(prev)))
    for f in os.listdir(BASE_MEDIA):
        if f != "manifest.json" and not os.path.exists(f"{M}/{f}"): os.symlink(f"{BASE_MEDIA}/{f}", f"{M}/{f}")
    for pm in glob.glob(f"{ROOT}/media_ep*/"):
        for f in os.listdir(pm):
            if f != "manifest.json" and not os.path.lexists(f"{M}/{f}"): os.symlink(os.path.realpath(f"{pm}/{f}"), f"{M}/{f}")
    from PIL import Image
    for js in sorted(glob.glob(f"{src}/*.json")):
        k = os.path.basename(js)[:-5]; ii = json.load(open(js)); em = ii.get("extmetadata", {})
        raw = [p for p in glob.glob(f"{src}/{k}.*") if not p.endswith(".json")][0]
        if k.startswith("img_"):
            dst = f"{k}.jpg"; Image.open(raw).convert("RGB").save(f"{M}/{dst}", quality=95); typ = "image"
        else:
            dst = f"{k}.mp4"; typ = "video"
            sh("ffmpeg", "-v", "error", "-y", "-i", raw, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", f"{M}/{dst}")
        if os.path.islink(f"{M}/{dst}"): pass
        d = dict(type=typ, file=dst, author=strip(em.get("Artist", {}).get("value")), license=strip(em.get("LicenseShortName", {}).get("value")),
                 site="Wikimedia Commons", page=ii.get("descriptionurl"))
        if typ == "video": d["duration"] = round(float(out("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{M}/{dst}")))
        if d["author"].startswith("[null") or not d["author"]: d["author"] = "U.S. Navy (DVIDS)" if "dvids" in json.dumps(em).lower() else "U.S. Department of Defense"
        if "Avash" in (ii.get("descriptionurl") or ""): d["author"] = "Mohammad Berno / Avash News Agency" if "%D8%A8%D8%B1%D9%86%D9%88" in json.dumps(em) or "برنو" in d["author"] else d["author"] + " / Avash News Agency"
        man[k] = d; print("ingest", k, d["author"][:40], d["license"])
    json.dump(man, open(f"{M}/manifest.json", "w"), ensure_ascii=False, indent=1)

def audio(ep, src):
    E, W, M = dirs(ep)
    for L in ("en", "jp"):
        os.makedirs(f"{W}/audio/{L}", exist_ok=True)
        for f in glob.glob(f"{src}/{L}/*.mp3"): shutil.copy(f, f"{W}/audio/{L}/")
        print(L, len(glob.glob(f"{W}/audio/{L}/*.mp3")))

def env(ep, L):
    E, W, M = dirs(ep)
    return dict(os.environ, EF_ROOT=W, EF_MEDIA=M, EF_CONTENT_DIR=W, EF_CONTENT=f"content_ep{E}_{L}", EF_AUDIO=f"{W}/audio/{L}", EF_OUT=f"{W}/out/{L}", EF_TMP=f"{W}/tmp/{L}")

def tts_ko(ep):
    E, W, M = dirs(ep); os.makedirs(f"{W}/audio/ko", exist_ok=True)
    sh("python3", f"{KIT}/tts/tts_typecast_ko.py", env=env(ep, "ko"))

def durations(ep):
    for L in LANGS: sh("python3", f"{KIT}/tts/make_durations.py", L, env=env(ep, L))

def pending(ep):
    E, W, M = dirs(ep)
    return [(L, p) for L in LANGS for p in PLATS if not os.path.exists(f"{W}/out/{L}/epic_fury_ep{E}_{p}_{L}.mp4")]

def est_min(ep, L, p):  # ~4.6 min of render per minute of 4K video on 2 cores
    E, W, M = dirs(ep); d = json.load(open(f"{W}/audio/{L}/durations.json"))
    if p == "longform_mobile": return 10  # 16:9 longform scaled to 1920x1080 (mobile16x9.py), not rendered
    K = importlib.import_module(f"content_ep{E}_{L}") if W in sys.path else (sys.path.insert(0, W), importlib.import_module(f"content_ep{E}_{L}"))[1]
    sec = sum(d[f"p{n:02d}"]["dur"] + 1.7 for n in K.PLATFORMS[p][2]) + d[f"cover_{p}"]["dur"] + d["end"]["dur"] + 3
    return sec / 60 * 5.6

def render(ep, budget=110):
    E, W, M = dirs(ep); t0 = time.time()
    for L, p in pending(ep):
        need = est_min(ep, L, p); used = (time.time() - t0) / 60
        if used + need > budget: print(f"STOP budget: next {L} {p} needs ~{need:.0f} min, used {used:.0f}"); return
        print(f"START {L} {p} (~{need:.0f} min) {time.strftime('%T')}", flush=True)
        if p == "longform_mobile":  # since 2026-11-04: original 16:9 longform format, scaled for phones
            r = subprocess.run(["python3", f"{ROOT}/pipeline/mobile16x9.py", "make", E, L], stdout=open(f"{W}/log_{L}.txt", "a"), stderr=subprocess.STDOUT)
        else:
            r = subprocess.run(["python3", f"{KIT}/render/render_v3_{L}.py", p], env=env(ep, L), stdout=open(f"{W}/log_{L}.txt", "a"), stderr=subprocess.STDOUT)
        (r.returncode == 0) and shutil.rmtree(f"{W}/tmp/{L}/{p}", ignore_errors=True)
        print(("DONE" if r.returncode == 0 else "FAIL"), L, p, time.strftime("%T"), flush=True)
        if r.returncode: return
    print("ALLDONE" if not pending(ep) else "BATCHDONE")

def git_push(repo, paths, msg):
    os.chdir(repo); sh("git", "add", "--sparse", *paths)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode:
        sh("git", *GIT, "commit", "-qm", msg + TRAILER)
    sh("git", "pull", "-q", "--rebase", "--autostash"); sh("git", "push", "-q")
    return out("git", "log", "-1", "--format=%H").strip()

def upload(ep, langs):
    E, W, M = dirs(ep)
    os.chdir("/home/claude/videos"); sh("git", "pull", "-q", "--rebase", "--autostash")
    for L in langs:
        D = f"novel/ep{E}/platform_{L}"; os.makedirs(D, exist_ok=True)
        for f in glob.glob(f"{W}/out/{L}/*.mp4"):
            b = os.path.basename(f)
            if os.path.exists(f"{D}/{b}") and hashlib.md5(open(f, "rb").read()).digest() == hashlib.md5(open(f"{D}/{b}", "rb").read()).digest(): continue
            shutil.copy(f, D)
            if os.path.getsize(f) > 95_000_000: sh("git", "lfs", "track", f"{D}/{b}", stdout=subprocess.DEVNULL)
    sha = git_push("/home/claude/videos", [".gitattributes", f"novel/ep{E}"], f"EP{E} platform MP4s ({' '.join(langs)})")
    subprocess.run(["git", "lfs", "prune", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir("/home/claude/assets"); sh("git", "pull", "-q", "--rebase", "--autostash")
    for L in langs:
        D = f"novel/ep{E}/platform_{L}"; os.makedirs(D, exist_ok=True)
        for f in glob.glob(f"{W}/out/{L}/*.srt"): shutil.copy(f, D)
    git_push("/home/claude/assets", [f"novel/ep{E}"], f"EP{E} platform subtitles ({' '.join(langs)})")
    os.chdir("/home/claude/audio"); sh("git", "pull", "-q", "--rebase", "--autostash")
    for L in langs:
        D = f"novel/ep{E}/{L}_v2"; os.makedirs(D, exist_ok=True)
        for f in glob.glob(f"{W}/audio/{L}/*"): shutil.copy(f, D)
    git_push("/home/claude/audio", [f"novel/ep{E}"], f"EP{E} platform narration ({' '.join(langs)})")
    print("videos", sha)

def manifest(ep):
    E, W, M = dirs(ep); os.chdir("/home/claude/videos"); sha = out("git", "log", "-1", "--format=%H").strip()
    files = []
    for p in sorted(glob.glob(f"novel/ep{E}/platform_*/*.mp4")):
        base = "https://media.githubusercontent.com/media" if out("git", "check-attr", "filter", "--", p).strip().endswith("lfs") else "https://raw.githubusercontent.com"
        files.append(dict(url=f"{base}/soulthread88/videos/{sha}/{p}", name=os.path.basename(p), sub=p.split("/")[2], md5=hashlib.md5(open(p, "rb").read()).hexdigest()))
    os.chdir("/home/claude/assets"); sh("git", "pull", "-q", "--rebase", "--autostash"); os.makedirs(f"novel/ep{E}", exist_ok=True)
    json.dump(dict(ep=E, videos_commit=sha, files=files), open(f"novel/ep{E}/sync_manifest.json", "w"), indent=1)
    a = git_push("/home/claude/assets", [f"novel/ep{E}/sync_manifest.json"], f"EP{E} sync manifest ({len(files)} MP4s)")
    print(f"https://raw.githubusercontent.com/soulthread88/assets/{a}/novel/ep{E}/sync_manifest.json")

def status(ep):
    E, W, M = dirs(ep); p = pending(ep); print(f"EP{E}: {27 - len(p)}/27 done; pending: {p}")

if __name__ == "__main__":
    c, ep = sys.argv[1], sys.argv[2]; a = sys.argv[3:]
    dict(ingest=lambda: ingest(ep, a[0]), audio=lambda: audio(ep, a[0]), **{"tts-ko": lambda: tts_ko(ep)}, durations=lambda: durations(ep),
         render=lambda: render(ep, float(a[0]) if a else 110), upload=lambda: upload(ep, a), manifest=lambda: manifest(ep), status=lambda: status(ep))[c]()
