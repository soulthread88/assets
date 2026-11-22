#!/usr/bin/env python3
"""Film a render-mode HTML into an MP4: thumbnail first, then one held still per caption cue,
scene crossfades inside the segment, stock 4K video b-roll under the UI overlay on scene openers.
usage: render.py <render.html> <narration.mp3> <out.mp4> [--frames-only]"""
import sys, os, json, re, subprocess, asyncio, shutil
from playwright.async_api import async_playwright

THUMB_SEC = 2.5
FPS = 30
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-r", str(FPS),
        "-x264-params", "keyint=300:min-keyint=30", "-tune", "stillimage"]
STOCK = os.path.abspath("build/stock")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(" ".join(cmd[:8]) + "\n" + r.stderr[-800:])


async def shoot(html, outdir):
    src = open(html, encoding="utf-8").read()
    data = json.loads(re.search(r"const D=(\{.*?\});\n", src, re.S).group(1))
    W, H = data["W"], data["H"]
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome",
                                    args=["--allow-file-access-from-files", "--disable-gpu", "--hide-scrollbars"])
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        await pg.goto("file://" + os.path.abspath(html) + "#thumb")
        await pg.add_style_tag(content="body.render .bg{transition:none!important}")
        await pg.wait_for_function("document.body.dataset.ready==1")
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=f"{outdir}/thumb.jpg", type="jpeg", quality=92)
        await pg.evaluate("location.hash='f=0'")
        last_scene = None
        for i, c in enumerate(data["cues"]):
            await pg.evaluate(f"location.hash='f={i}'")
            if c["s"] != last_scene:
                await pg.evaluate("Promise.all([...document.querySelectorAll('.bg')].map(e=>{const u=(e.style.backgroundImage.match(/url\\(\"(.*)\"\\)/)||[])[1];if(!u)return;const im=new Image();im.src=u;return im.decode().catch(()=>{})}))")
                await pg.wait_for_timeout(150)
            await pg.screenshot(path=f"{outdir}/c{i:04d}.jpg", type="jpeg", quality=92)
            if c["s"] != last_scene:  # transparent UI overlay for b-roll
                await pg.add_style_tag(content="#bgs{visibility:hidden} html,body,#wrap{background:transparent!important}")
                await pg.screenshot(path=f"{outdir}/o{i:04d}.png", omit_background=True)
                await pg.evaluate("document.querySelectorAll('style')[document.querySelectorAll('style').length-1].remove()")
            last_scene = c["s"]
        await b.close()
    return data


def seg_still(img, dur, out, prev=None, fade=0.6):
    tmp = out[:-4] + ".tmp.mp4"
    if prev and dur > fade + 0.2:
        run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", prev, "-framerate", str(FPS), "-i", img,
             "-filter_complex", f"[0]format=yuv420p,loop=-1:1,trim=duration={fade}[a];[1]format=yuv420p,loop=-1:1,trim=duration={dur}[b];"
                                f"[a][b]xfade=transition=fade:duration={fade}:offset=0,trim=duration={dur},setpts=PTS-STARTPTS",
             *VENC, "-an", tmp])
    else:
        run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", img, "-vf",
             f"format=yuv420p,loop=-1:1,trim=duration={dur},setpts=PTS-STARTPTS", *VENC, "-an", tmp])
    os.replace(tmp, out)


def seg_broll(video, overlay, dur, W, H, out):
    tmp = out[:-4] + ".tmp.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", video, "-framerate", str(FPS), "-i", overlay,
         "-filter_complex", f"[0]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},eq=brightness=0.04:saturation=1.08,fps={FPS},"
                            f"trim=duration={dur},setpts=PTS-STARTPTS,fade=in:st=0:d=0.5[v];[1]format=rgba,loop=-1:1,trim=duration={dur}[o];"
                            f"[v][o]overlay=0:0:format=auto,format=yuv420p",
         *[x for x in VENC if x not in ("-tune", "stillimage")], "-an", "-t", str(dur), tmp])
    os.replace(tmp, out)


def main(html, audio, out, frames_only=False):
    work = out[:-4] + "_work"
    os.makedirs(work, exist_ok=True)
    data = asyncio.run(shoot(html, work))
    if frames_only:
        return
    W, H, cues = data["W"], data["H"], data["cues"]
    orient = "landscape" if W > H else "portrait"
    audio_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                               "-of", "csv=p=0", audio]).decode())
    segs = [f"{work}/s_thumb.mp4"]
    if not os.path.exists(segs[0]):
        seg_still(f"{work}/thumb.jpg", THUMB_SEC, segs[0])
    t0 = 0.0
    last_scene, prev = None, f"{work}/thumb.jpg"
    for i, c in enumerate(cues):
        a = 0.0 if i == 0 else c["a"]
        b = audio_dur + 1.5 if i == len(cues) - 1 else cues[i + 1]["a"]
        dur = round(b - a, 3)
        segf = f"{work}/s{i:04d}.mp4"
        img = f"{work}/c{i:04d}.jpg"
        scene = data["scenes"][c["s"]]
        vid = f"{STOCK}/{scene['bg']}_{orient}.mp4"
        if not os.path.exists(segf):
            if c["s"] != last_scene and os.path.exists(vid) and dur >= 2.0:
                seg_broll(vid, f"{work}/o{i:04d}.png", dur, W, H, segf)
            else:
                seg_still(img, dur, segf, prev if c["s"] != last_scene else None)
        segs.append(segf)
        last_scene, prev = c["s"], img
    with open(f"{work}/list.txt", "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-c", "copy", f"{work}/video.mp4"])
    tmp = out[:-4] + ".tmp.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/video.mp4", "-i", audio, "-filter_complex",
         f"[1]adelay={int(THUMB_SEC*1000)}|{int(THUMB_SEC*1000)},apad[a]", "-map", "0:v", "-map", "[a]",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp])
    os.replace(tmp, out)
    print("done", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], "--frames-only" in sys.argv)
