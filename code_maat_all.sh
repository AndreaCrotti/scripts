#!/usr/bin/env bash

CODE_MAAT="java -jar $HOME/scripts/code-maat-1.0-SNAPSHOT-standalone.jar"
LOGFILE="logfile.log"
echo "generating logfile to $LOGFILE"
git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > $LOGFILE

# messages requires an extra argument
OPS="abs-churn age author-churn authors communication coupling entity-churn entity-effort entity-ownership fragmentation identity main-dev main-dev-by-revs refactoring-main-dev revisions soc"

for op in $OPS; do
    echo "running $op"
    $CODE_MAAT -c git2 -l $LOGFILE -a $op > $op.csv
done
