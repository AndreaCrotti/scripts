#!/usr/bin/env bash

for branch in $(git branch --merged master | grep -v master)
do
    git branch -d $branch
done
