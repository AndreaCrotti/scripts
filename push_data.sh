#!/bin/bash

SERVER=$1
OPTS=$2


# making sure we start from the right directory
cd $HOME

# TODO put a filter for the org directory
FILES=$(cat $HOME/bin/files.txt)
EXCLUDE="$HOME/bin/exclude_list"

OPTS="-avz --relative -e $OPTS"

echo $FILES
for x in $FILES
do
    if test -d $x
    then OP="--delete-after $OPTS"
    else OP=$OPTS
    fi
    CMD="rsync $OP $x $SERVER:"
    echo "executing $CMD"
#    $CMD
done

