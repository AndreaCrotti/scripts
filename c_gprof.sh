#!/bin/bash
# change those variables as you prefer
PROG=$1
PROF="gmon.out"
STATS=$1.stats
TYPE=png
OUT=profiled.$TYPE
OPEN="open"
set -x

./$@
gprof $PROG | gprof2dot.py | dot -T$TYPE -o $OUT
$OPEN $OUT