#!/bin/bash

SERVER=$1
OPT=$2

# making sure we start from the right directory
cd $HOME

# TODO put a filter for the org directory
FILES=$(cat $HOME/scripts/files.txt)
EXCLUDE="$HOME/scripts/exclude_list"

# now it's using ssh (no need of rsync server)
CMD="rsync -avz $OPT --exclude-from=$HOME/scripts/exclude_list --relative $FILES $SERVER:$SHARE"

echo "executing $CMD"

$CMD
