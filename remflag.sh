#!/bin/bash
DST=$1
# all the rests are extensions

find $DST -iname '*.html' | xattr -d com.apple.quarantine