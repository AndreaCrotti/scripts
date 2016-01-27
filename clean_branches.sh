#!/usr/bin/env bash

for branch in $(git branch --merged master); do git branch -d $branch; done
