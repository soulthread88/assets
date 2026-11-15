import make_blogs_all as M, os, subprocess, json
from PIL import Image, ImageStat
W="/home/claude/work"; OUT="/home/claude/imgs/novel"
def used(N):
    keys=M.media_keys(N); d=M.parse(N,"ko"); rest=keys[2:] or keys
    sk=[rest[(i*len(rest))//max(1,len(d["scenes"]))] for i in range(len(d["scenes"]))]
    return list(dict.fromkeys([keys[0], keys[1%len(keys)]]+sk))
def bright(p): return sum(ImageStat.Stat(Image.open(p).convert("L").resize((64,36))).mean)
log={}
for n in range(1,11):
    N=f"{n:02d}"; MAN=M.man(N); md=f"{W}/media_ep{N}" if N!="01" else f"{W}/media"
    od=f"{OUT}/ep{N}/blog"; os.makedirs(od,exist_ok=True); log[N]=[]
    for k in M.media_keys(N):
        src=os.path.join(md,MAN[k]["file"]); o=f"{od}/{k}.jpg"
        if os.path.exists(o): log[N].append((k,round(bright(o)))); continue
        vf="scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160"
        if src.lower().endswith((".jpg",".jpeg",".png",".webp")):
            subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf",vf,"-q:v","3",o],check=True)
        else:
            best=None
            for t in (3,6,10,1):
                tmp=o+f".{t}.jpg"
                r=subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",src,"-frames:v","1","-vf",vf,"-q:v","3",tmp])
                if r.returncode or not os.path.exists(tmp): continue
                b=bright(tmp)
                if best is None or b>best[0]: best=(b,tmp)
                if b>70: break
            os.replace(best[1],o)
            for t in (3,6,10,1):
                if os.path.exists(o+f".{t}.jpg"): os.remove(o+f".{t}.jpg")
        log[N].append((k,round(bright(o))))
    print(N, len(log[N]))
json.dump(log,open('/home/claude/work/blogs/bright.json','w'))
