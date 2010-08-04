#!/bin/bash

# bar script by Oscar Dustmann - 2010
# you need `bash` and `watch` to run this

if [ "$1" = "bar" ]
then
  shift
  starttime="$1"
  totaltime="$2"
  end=$(date +%s)
  diff="$[ $end - $starttime ]"

  width="${COLUMNS}"
  lines="$width"

  b=$[ ($diff * $width)/$totaltime ]
  i=0
  out="$(printf "%${b}s\n" "|")"
  if [ $totaltime -le $width ]
  then
    # ensure gapless display for small periods
    out="$(echo "$out" | tr ' ' '.')"
  fi
  while [ $i -lt $lines ]
  do
    i=$[ $i + 1 ]
    echo "$out"
  done
else
  if [ "$1" = '' ]
  then
    echo "Call me with a time in seconds. E.g. for 10 minutes execute:"
    echo "$0 600"
    exit 1
  fi
  totaltime="$1"
  starttime="$(date +%s)"
  screenwidth="${COLUMNS}"
  watch -t -n 1 -p --differences=cumulative  -- "$0 bar $starttime $totaltime"
fi
