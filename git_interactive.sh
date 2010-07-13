#! /bin/bash
# taken from http://stackoverflow.com/questions/449541/how-do-you-merge-selective-files-with-git-merge
# git-interactive-merge
from=$1
to=$2
git checkout $from
git checkout -b ${from}_tmp
git rebase -i $to
# Above will drop you in an editor and pick the changes you want
git checkout $to
git pull . ${from}_tmp
git branch -d ${from}_tmp