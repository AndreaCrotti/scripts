#!/usr/bin/env bash

set -ex

REPO=$1
OUT=$2

gource $REPO \
    -s .03 \
    -1280x720 \
    --auto-skip-seconds .1 \
    --multi-sampling \
    --stop-at-end \
    --key \
    --highlight-users \
    --date-format "%d/%m/%y" \
    --hide mouse,filenames \
    --file-idle-time 0 \
    --max-files 0  \
    --background-colour 000000 \
    --font-size 25 \
    --output-ppm-stream - \
    --output-framerate 30 \
    | ffmpeg -y -r 30 -f image2pipe -vcodec ppm -i - -b 65536K $OUT.mp4


# gource $REPO \
#        --800x600 \
#        --max-files 99999 \
#        --disable-progress \
#        --stop-at-end \
#        -s 0.25 \
#        --user-scale 2 \
#        --highlight-all-users \
#        --output-ppm-stream - | ffmpeg -y \
#                                        -r 60 \
#                                        -f image2pipe \
#                                        -vcodec ppm \
#                                        -i -- -vcodec libx264 \
#                                        $OUT.mp4

#                                        # -b 3000K \
