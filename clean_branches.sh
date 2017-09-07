#!/usr/bin/env bash

BASE=$1

for branch in $(git branch --merged $BASE | grep -v $BASE)
do
    git branch -d $branch
done
