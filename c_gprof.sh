#!/bin/bash
# change those variables as you prefer
PROG=$1
PROF="gmon.out"
TYPE=pdf
OUT=profiled.$TYPE

if uname | grep -i 'darwin'
then
    GPROF2DOT="gprof2dot.py"
elif uname | grep -i 'linux'
then
    GPROF2DOT="gprof2dot"
fi

set -x

./$@
gprof $PROG | $GPROF2DOT -e0 -n0 | dot -T$TYPE -o $OUT
echo "now open $OUT"