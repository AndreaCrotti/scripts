#!/usr/bin/env bash

CODE_MAAT="java -jar $HOME/scripts/code-maat-1.0-SNAPSHOT-standalone.jar"
LOGFILE="logfile.log"
echo "generating logfile to $LOGFILE"
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > $LOGFILE

OPS="abs-churn age author-churn authors communication coupling entity-churn entity-effort entity-ownership fragmentation identity main-dev main-dev-by-revs messages refactoring-main-dev revisions soc summary"

for op in $OPS; do
    echo "running $op"
    $CODE_MAAT -c git2 -l $LOGFILE -a $op > $op.csv
done
