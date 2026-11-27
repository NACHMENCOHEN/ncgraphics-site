#!/bin/bash
# Usage: ./make.sh [YYYY-MM-DD]  -> builds Shabbat video for the coming Shabbat
set -e; cd "$(dirname "$0")"; T=12
python3 zm.py ${1:-} >/dev/null
python3 build.py $T
node render.js $T video.mp4
python3 music.py $T
D=$(python3 -c "import json;print(json.load(open('week.json'))['date'])")
ffmpeg -y -v error -i video.mp4 -i music.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart "Shabbat-$D.mp4"
echo "Shabbat-$D.mp4"
