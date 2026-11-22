#!/usr/bin/env bash
# Upload final MP4s (too large for git) to the soulthread88/videos Release "life-ep01". usage: release.sh <lang>
set -euo pipefail
L=$1; cd /home/claude/life
env -u GH_TOKEN gh release view life-ep01 -R soulthread88/videos >/dev/null 2>&1 || \
  env -u GH_TOKEN gh release create life-ep01 -R soulthread88/videos --title "Life Story EP01 · 4K videos (KO/EN/JP)" \
  --notes "4K MP4 renders for Life Story EP01. Landscape 3840x2160 (YouTube long form / Facebook / X, PC + mobile-safe), vertical 2160x3840 (Shorts / Reels / TikTok, PC + mobile-safe), 2160x2700 (Threads / Instagram feed). Thumbnail first. Background media: Pexels License."
for f in build/$L/out/*.mp4; do env -u GH_TOKEN gh release upload life-ep01 "$f" -R soulthread88/videos --clobber; echo "uploaded $f"; done
