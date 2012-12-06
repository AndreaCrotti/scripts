#!/bin/bash
# take a source repository, copy it, clean it and compute the sloccounts
set -x

REV_HASH=$(git rev-list master --reverse)

function slocc {
    echo "Rev $1 =  $(sloccount . | grep 'Total Physical')"
}

function iter_loc {
    for commit in $REV_HASH
    do
        git checkout $commit
        git clean -xdf
        slocc $commit
    done
}

DEST_REPO=$1
DEST_TMP="/tmp/$DEST_REPO"
cp -Rv $DEST_REPO $DEST_TMP
cd $DEST_TMP

iter_loc
