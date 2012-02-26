#!/bin/bash
# input_file=$1
revs=$(git rev-list --reverse master)

# [ -f $input_file ] || exit 1

for rev in $revs; do
    # echo "checking out revision $rev"
    clear
    git checkout $rev
    git clean -df
    ls -l
    sleep 3
    # head -n 30 $input_file
done
