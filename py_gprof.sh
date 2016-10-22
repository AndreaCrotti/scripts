#!/bin/bash
FNAME=$1
if [ ! -f $FNAME ]
then
    echo "file $FNAME not found, executing from $PWD"
    exit 1
fi
# discard filename
shift

# change those variables as you prefer
STATS="output.pstats"
TYPE=png
OUT=output.$TYPE

if uname | grep -i 'darwin'
then
    OPEN="open"
    GPROF2DOT="gprof2dot.py"
elif uname | grep -i 'linux'
then
    OPEN="evince"
    GPROF2DOT="gprof2dot"
fi

# $@ collect all the arguments for the python script
# it doens't contain the file name after the shift
python -m cProfile -o $STATS $FNAME $@
$GPROF2DOT -f pstats $STATS | dot -T$TYPE -o $OUT
rm $STATS
$OPEN $OUT
