#!/bin/bash

SERVER="koalawlan"
SHARE="data"
OPTIONS=$1

if ! fping -a $SERVER
then
    echo "server $SERVER not reachable"
    exit 1
fi    
    

# making sure we start from the right directory
cd $HOME

# TODO put a filter for the org directory
FILES=$(cat $HOME/scripts/files.txt)
EXCLUDE="$HOME/scripts/exclude_list"

CMD="rsync -avz $OPTIONS --exclude-from=$HOME/scripts/exclude_list --delete --relative $FILES $SERVER::$SHARE"

echo "executing $CMD"

$CMD
