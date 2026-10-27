import requests,time,json,os,subprocess,re,sys
S=requests.Session(); S.headers["User-Agent"]="EpicFuryProduction/1.0 (heewoo.kim@gmail.com)"
want={
 "img_b2_depart":"File:B-2 Spirit stealth bomber departs in support of Operation Epic Fury (9595923).jpg",
 "img_f15e":"File:An F-15E Strike Eagle Takes Off for Combat Flight (9582604).jpg",
 "img_f16_fly":"File:F-16 Fighting Falcons fly during Operation Epic Fury (9597865).jpg",
 "img_hornet":"File:F-A-18E Super Hornet Conducts Flight Operations (9591855).jpg",
 "img_tehran_smoke":"File:Attack on areas north of Tehran 1 Avash 20 esfand 1404.webp",
 "img_borujerdi4":"File:Airstrike on the residential town of Shahid Boroujerdi 4 Avash.webp",
 "img_borujerdi8":"File:Effects of airstrike on Shahid Borujerdi Town (8).jpg",
 "img_map100h":'File:2026 map of "Operation Epic Fury Timeline - First 100 Hours" used during press briefing at the Pentagon, Arlington, Virginia on 4 March (cropped).jpg',
 "img_iran_launch_map":"File:Iranian missile and drone launches during the 2026 Iran war.svg",
 "img_spruance":"File:USS Spruance launching Tomahawk during Operation Epic Fury.jpg",
 "img_ford_deck":"File:USS Gerald R Ford (CVN 78) Conducts Flight Operations During Operation Epic Fury (9559679).jpg",
 "img_b2_prep":"File:A B-2 Spirit stealth bomber prepares to take off during Operation Epic Fury (9573730).jpg",
}
def strip(h): return re.sub("<[^>]+>","",h or "").strip()
def get(url,**kw):
    for a in range(25):
        r=S.get(url,**kw)
        if r.status_code==200: return r
        time.sleep(40)
    raise Exception('gave up')
for k,t in want.items():
    man=json.load(open('media/manifest.json'))
    if man.get(k,{}).get('author'): continue
    r=get("https://commons.wikimedia.org/w/api.php",params=dict(action="query",titles=t,prop="imageinfo",iiprop="url|size|extmetadata",iiurlwidth=3840,format="json"))
    ii=next(iter(r.json()['query']['pages'].values()))['imageinfo'][0]; md=ii['extmetadata']
    meta=dict(type="image",title=t[5:],width=ii['width'],height=ii['height'],author=strip(md.get('Artist',{}).get('value')),
      license=strip(md.get('LicenseShortName',{}).get('value')),date=strip(md.get('DateTimeOriginal',{}).get('value')),
      site="Wikimedia Commons",page=ii['descriptionurl'])
    ext='.png' if t.endswith('.svg') else '.jpg'; dst=f"media/{k}{ext}"
    if not os.path.exists(dst):
        url=ii['thumburl'] if (ii['width']>3840 or t.endswith('.webp') or t.endswith('.svg')) else ii['url']
        time.sleep(5); b=get(url)
        open(dst+'.src','wb').write(b.content)
        subprocess.run(['ffmpeg','-v','error','-y','-i',dst+'.src','-q:v','2',dst],check=True); os.remove(dst+'.src')
        meta['source_url']=url
    else:
        meta['source_url']=man.get(k,{}).get('source_url',ii['url'])
    meta['file']=os.path.basename(dst)
    man=json.load(open('media/manifest.json')); man[k]=meta
    json.dump(man,open('media/manifest.json','w'),ensure_ascii=False,indent=1)
    print('OK',k,meta['width'],meta['author'],meta['license'],flush=True); time.sleep(10)
print('DONE')
