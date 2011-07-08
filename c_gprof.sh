#!/bin/bash

# TODO: add some trapping mechanism to catch errors

PROG=$1
PROF="gmon.out"
TYPE=pdf
OUT=profiled.$TYPE

if [ $# -lt 1 ]
then 
    echo "usage $0 <program> [arguments...]"
    exit 1
fi

   
if uname | grep -i 'darwin'
then
    GPROF2DOT="gprof2dot.py"
else
    GPROF2DOT="gprof2dot"
fi

./$@
gprof $PROG | $GPROF2DOT -e0 -n0 | dot -T$TYPE -o $OUT
echo "graph in $OUT"
