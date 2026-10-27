#!/bin/sh
# tile.sh video.mp4 out.jpg -> one frame every 0.5 s (check every ad with this before delivering)
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -loglevel error -y -i "$1" -vf "select='not(mod(n\,15))',scale=108:192,tile=20x3:color=white:padding=2" -frames:v 1 "$2"
