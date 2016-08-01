#!/bin/bash

# make sure that you have compiled the program with profiling flage
# (-pg for gcc) and that you have gprof2dot in your path
#
# TODO: add some trapping mechanism to catch errors

PROF="gmon.out"
TYPE=pdf
OUT=profiled.$TYPE

if [ $# -lt 1 ]
then 
    echo "usage $0 <program> [arguments...]"
    exit 1
fi

PROG=$1
   
if uname | grep -i 'darwin'
then
    GPROF2DOT="gprof2dot.py"
else
    GPROF2DOT="gprof2dot"
fi

./$@
gprof $PROG | $GPROF2DOT -e0 -n0 | dot -T$TYPE -o $OUT
echo "Result graph is in $OUT"

