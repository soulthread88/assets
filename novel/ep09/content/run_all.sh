#!/bin/bash
# EP09 프레임 렌더 큐 (재시작 가능: 끝난 MP4와 세그먼트는 건너뜀)
cd /home/claude/work/ep09
for L in ko en jp; do
 for P in shorts longform tiktok reels threads x facebook feeds; do
  [ -f out/$L/epic_fury_ep09_${P}_$L.mp4 ] && continue
  echo "START $L $P $(date -u +%T)"
  EF_CONTENT=content_ep09_$L EF_CONTENT_DIR=/home/claude/work/ep09/flat EF_MEDIA=/home/claude/work/media_ep09 EF_AUDIO=/home/claude/work/ep09/audio/$L \
  EF_OUT=/home/claude/work/ep09/out/$L EF_TMP=/home/claude/work/ep09/tmp/$L python3 /home/claude/work/pipeline/render_frame.py $P > logs_${L}_${P}.txt 2>&1 \
   && echo "DONE $L $P $(date -u +%T) $(grep DONE logs_${L}_${P}.txt | cut -c1-80)" || { echo "FAIL $L $P"; tail -3 logs_${L}_${P}.txt; }
 done
done
echo ALLDONE
