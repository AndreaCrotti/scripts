#!/bin/bash
# take a source repository, copy it, clean it and compute the sloccounts
function slocc {
    echo "Rev $1 =  $(sloccount . | grep 'Total Physical')"
}

function iter_loc {
    REV_HASH=$(git rev-list master --reverse)
    for commit in $REV_HASH
    do
        git checkout -f $commit > /dev/null
        git clean -xdf > /dev/null
        slocc $commit
    done
}

DEST_REPO=$1
DEST_TMP="/tmp/$DEST_REPO"
cp -R $DEST_REPO $DEST_TMP > /dev/null
cd $DEST_TMP

iter_loc
