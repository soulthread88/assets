#!/usr/bin/env bash
# lifestory publish stage: copy built assets into the five soulthread88 repos under life/ep01 and push.
# usage: publish.sh <lang>     (MP4 finals go to the videos repo Release "life-ep01" via release.sh)
set -euo pipefail
L=$1; ROOT=/home/claude/life; GH=/home/claude; EP=life/ep01
cd "$ROOT"
mkdir -p $GH/htmls/$EP/$L $GH/imgs/$EP/thumb $GH/audio/$EP/$L $GH/assets/$EP/$L $GH/assets/$EP/pipeline $GH/videos/$EP/broll
# HTML: platform video players (publish URLs) + full story + blogs
for k in shorts feed long; do python3 pipeline/build_html.py $L $k build/$L/$k/timeline.json $GH/htmls/$EP/$L publish >/dev/null; done
python3 pipeline/build_pages.py $L $GH/htmls/$EP/$L >/dev/null
# images (shared) + thumbnails
cp -n build/web/img/*.jpg $GH/imgs/$EP/ 2>/dev/null || true
cp build/thumbs/*-$L.jpg $GH/imgs/$EP/thumb/
# audio
for k in long shorts feed; do cp build/$L/$k/narration.mp3 $GH/audio/$EP/$L/lifestory-ep01-$k-$L.mp3; done
# assets: scripts, captions, timelines, credits, pipeline (no secrets)
for k in long shorts feed; do
  cp ep01/$L/$k.txt $GH/assets/$EP/$L/script-$k-$L.txt
  cp build/$L/$k/narration.srt $GH/assets/$EP/$L/captions-$k-$L.srt
  cp build/$L/$k/timeline.json $GH/assets/$EP/$L/timeline-$k-$L.json
done
cp ep01/$L/blogs.py $GH/assets/$EP/$L/blogs-$L.py
cp build/stock/manifest.json $GH/assets/$EP/stock-credits.json
cp pipeline/*.py pipeline/*.html pipeline/*.sh $GH/assets/$EP/pipeline/ 2>/dev/null || true
[ -f pipeline/n8n-lifestory-workflow.json ] && cp pipeline/n8n-lifestory-workflow.json $GH/assets/$EP/
# b-roll for the web players (each <25MB)
grep -q "broll done" build/broll.log 2>/dev/null && for f in build/broll/*.mp4; do [ -s "$f" ] && cp -n "$f" $GH/videos/$EP/broll/ || true; done
for r in htmls imgs audio assets videos; do
  cd $GH/$r
  git sparse-checkout add life >/dev/null 2>&1 || true
  git add -A life
  if ! git diff --cached --quiet; then
    git -c user.name="soulthread88" -c user.email="soulthread88@users.noreply.github.com" commit -q -m "lifestory ep01 ($L): $r assets

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PY7NmrFNMFXzJbSsQMNWxP"
    git -c push.negotiate=true push -q origin main 2>&1 | grep -v -i "negotiat" || true
    echo "pushed $r"
  fi
done
