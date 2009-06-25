#!/bin/bash
OTHER=$1
# making sure we start from the right directory
cd $HOME

# TODO put a filter for the org directory
FILES="Documents/blogging uni Documents/calzitex org Documents/languages scripts"
EXCLUDE="$HOME/scripts/exclude_list"

CMD="rsync -avz $OTHER --exclude-from=$HOME/scripts/exclude_list --delete --relative $FILES koalawlan::data"
echo "executing $CMD"
$CMD