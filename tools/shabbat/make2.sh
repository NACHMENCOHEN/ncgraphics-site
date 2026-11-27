#!/bin/bash
# Usage: ./make2.sh [clip.mp4|-] [YYYY-MM-DD]
#  clip: weekly video for the top area (best continuous 40s is picked automatically, with its sound).
#        "-" or nothing = no clip: candles / NC promo at the top and the NC song underneath.
set -e; cd "$(dirname "$0")"
CLIP="${1:--}"; DATE="${2:-}"
python3 zm.py $DATE >/dev/null
D=$(python3 -c "import json;print(json.load(open('week.json'))['date'])")
if [ "$CLIP" != "-" ]; then
  read S L < <(python3 pick.py "$CLIP" 40 | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['start'],d['len'])")
else S=0; L=36; fi
python3 - "$L" <<'PY'
import sys;d=open('week.json').read();T=sys.argv[1]
open('frame.html','w').write(open('template3.html').read().replace('__DATA__',d).replace('__TOTAL__',T))
PY
node render.js "$L" panel.mp4
OUT="Shabbat-$D.mp4"
if [ "$CLIP" != "-" ]; then
  HASA=$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$CLIP" | head -1)
  FO=$(python3 -c "print(max(0,$L-2))")
  if [ -n "$HASA" ]; then AIN="1:a"; else AIN="2:a"; fi
  ffmpeg -y -v error -i panel.mp4 -ss "$S" -t "$L" -i "$CLIP" -i song.m4a -filter_complex \
   "[1:v]scale=984:552:force_original_aspect_ratio=increase,crop=984:552,setsar=1,fps=30,fade=in:0:18[c];[0:v][c]overlay=48:48:shortest=1[v];[$AIN]atrim=0:$L,asetpts=N/SR/TB,loudnorm=I=-14:TP=-1.5,afade=t=in:d=0.8,afade=t=out:st=$FO:d=2[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  FO=$(python3 -c "print(max(0,$L-2))")
  ffmpeg -y -v error -i panel.mp4 -i song.m4a -filter_complex "[1:a]atrim=0:$L,loudnorm=I=-16,afade=t=in:d=1,afade=t=out:st=$FO:d=2[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart "$OUT"
fi
echo "$OUT (clip start $S, length $L)"
