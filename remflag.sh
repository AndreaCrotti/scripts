#!/bin/bash
# this script removes the quarantine flag from new files
# use with caution
if [ $# -lt 1 ]
then 
    echo "usage: ./$0 <dir1> ..."
    exit 1
fi


DST=$1
# all the rests are extensions

# TODO: make it really cycling the directories given 
find $DST -iname '*.html' | xattr -d com.apple.quarantine