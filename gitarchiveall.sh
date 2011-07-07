#!/usr/bin/env bash

# Script to archive all submodules in one big tar file

# TODO: make it general, taking submodules from command line

set -x
FMT=tar

TOPLEVEL="thesis.$FMT"

git archive --format=$FMT thesis.$FMT master
SUBMODS="inet_modified wifi-fw-realenv pad_mobility"

for sub in $SUBMODS
do
    FNAME="$sub.$FMT"
    (cd $sub && git archive --format=$FMT -o $FNAME master && mv $FNAME ..)
done

RESULT=pad_mobility_thesis.tar

tar -cvf $RESULT $TOPLEVEL

for sub in $SUBMODS
do
    tar -rvf $RESULT $sub.$FMT
done
