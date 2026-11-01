#!/bin/bash
# Render every missing EP01 platform video; safe to re-run (segments are cached).
cd /home/claude/work
while kill -0 1781 2>/dev/null; do sleep 20; done
for l in en jp; do for p in x facebook shorts reels tiktok threads feeds longform; do
  [ -f out_$l/epic_fury_ep01_${p}_$l.mp4 ] || python3 build/render_$l.py $p || echo FAIL $l $p
done; done
for p in feeds reels tiktok longform; do
  [ -f out2/.redo_$p ] || { python3 build/render_v2.py $p && touch out2/.redo_$p || echo FAIL ko $p; }
done
echo QUEUE_COMPLETE
