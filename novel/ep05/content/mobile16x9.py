#!/usr/bin/env python3
"""longform_mobile -> original 16:9 longform format (user decision 2026-11-04).
The 9:16 band version looked tiny on phones held sideways, so each longform_mobile MP4 is now the
regular 16:9 longform, scaled to 1920x1080 for phones. Same narration and timing, so the longform
subtitle file is reused for longform_mobile.

  python3 mobile16x9.py make  EP... [LANG]  # build out/<L>/epic_fury_epNN_longform_mobile_<L>.mp4 (resumable)
  python3 mobile16x9.py push  EP...   # commit to videos (LFS) + assets (srt)
Source longform: /home/claude/work/epNN/out/<L>/ if present, else pulled from the videos repo."""
import os, sys, subprocess, shutil, json
ROOT = "/home/claude/work"; VID = "/home/claude/videos"; AST = "/home/claude/assets"
LANGS = ["en", "jp", "ko"]
GIT = ["-c", "user.name=soulthread88", "-c", "user.email=heewoo.kim@gmail.com"]
TRAILER = "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01PY7NmpQMmmge1DdA9jzQEc"
def sh(*a, **k): return subprocess.run(a, check=True, **k)
def out(*a, **k): return subprocess.check_output(a, **k).decode()
def probe(p):
    j = json.loads(out("ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", p))
    return j["streams"][0]["width"], j["streams"][0]["height"], float(j["format"]["duration"])

def source(E, L):
    loc = f"{ROOT}/ep{E}/out/{L}/epic_fury_ep{E}_longform_{L}.mp4"
    if os.path.exists(loc): return loc, False
    rel = f"novel/ep{E}/platform_{L}/epic_fury_ep{E}_longform_{L}.mp4"
    os.chdir(VID); sh("git", "sparse-checkout", "add", "/" + rel)
    sh("git", "lfs", "pull", "--include", rel)
    p = f"{VID}/{rel}"; assert os.path.getsize(p) > 10_000_000, p
    return p, True

def make(E):
    for L in LANGS:
        d = f"{ROOT}/ep{E}/out/{L}"; os.makedirs(d, exist_ok=True)
        dst = f"{d}/epic_fury_ep{E}_longform_mobile_{L}.mp4"
        if os.path.exists(dst) and os.path.exists(dst + ".ok"): print("have", dst, flush=True); continue
        src, pulled = source(E, L)
        sw, shh, sd = probe(src); assert (sw, shh) == (3840, 2160), (src, sw, shh)
        tmp = dst + ".part.mp4"
        sh("ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", tmp)
        w, h, dd = probe(tmp); assert (w, h) == (1920, 1080) and abs(dd - sd) < 0.5, (w, h, dd, sd)
        os.replace(tmp, dst); open(dst + ".ok", "w").write(str(dd))
        srt = f"{AST}/novel/ep{E}/platform_{L}/epic_fury_ep{E}_longform_{L}.srt"
        if not os.path.exists(srt):
            os.chdir(AST); sh("git", "sparse-checkout", "add", f"/novel/ep{E}/platform_{L}/")
        shutil.copy(srt, f"{d}/epic_fury_ep{E}_longform_mobile_{L}.srt")
        if pulled:  # free the 4K source again
            os.chdir(VID); os.remove(src)
            sh("git", "update-index", "--skip-worktree", os.path.relpath(src, VID))  # local copy only; never commit a deletion
            subprocess.run(["git", "lfs", "prune", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("made", dst, f"{dd:.1f}s", os.path.getsize(dst) // 1_000_000, "MB", flush=True)

def push(eps):
    os.chdir(VID); sh("git", "pull", "-q", "--rebase", "--autostash")
    paths = []
    for E in eps:
        for L in LANGS:
            rel = f"novel/ep{E}/platform_{L}/epic_fury_ep{E}_longform_mobile_{L}.mp4"
            os.makedirs(os.path.dirname(rel), exist_ok=True)
            shutil.copy(f"{ROOT}/ep{E}/out/{L}/epic_fury_ep{E}_longform_mobile_{L}.mp4", rel)
            if os.path.getsize(rel) > 95_000_000 and not out("git", "check-attr", "filter", "--", rel).strip().endswith("lfs"):
                sh("git", "lfs", "track", rel, stdout=subprocess.DEVNULL)
            paths.append(rel)
    sh("git", "add", "--sparse", ".gitattributes", *paths)
    sh("git", *GIT, "commit", "-qm", f"Mobile longform back to 16:9 longform format, 1920x1080 (EP{', EP'.join(eps)})" + TRAILER)
    sh("git", "pull", "-q", "--rebase", "--autostash"); sh("git", "push", "-q")
    print("videos", out("git", "log", "-1", "--format=%H").strip())
    os.chdir(AST); sh("git", "pull", "-q", "--rebase", "--autostash"); sp = []
    for E in eps:
        for L in LANGS:
            rel = f"novel/ep{E}/platform_{L}/epic_fury_ep{E}_longform_mobile_{L}.srt"
            os.makedirs(os.path.dirname(rel), exist_ok=True)
            shutil.copy(f"{ROOT}/ep{E}/out/{L}/epic_fury_ep{E}_longform_mobile_{L}.srt", rel); sp.append(rel)
    sh("git", "add", "--sparse", *sp)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode:
        sh("git", *GIT, "commit", "-qm", f"Mobile longform subtitles = longform timing (EP{', EP'.join(eps)})" + TRAILER)
        sh("git", "pull", "-q", "--rebase", "--autostash"); sh("git", "push", "-q")
    print("assets", out("git", "log", "-1", "--format=%H").strip())

if __name__ == "__main__":
    a = sys.argv[2:]
    if a and a[-1] in LANGS: LANGS[:] = [a.pop()]  # e.g. "make 06 ko" from ef_pipeline render
    cmd, eps = sys.argv[1], ["%02d" % int(x) for x in a]
    if cmd == "make":
        for E in eps: make(E)
    elif cmd == "push": push(eps)
