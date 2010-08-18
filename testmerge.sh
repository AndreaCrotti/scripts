#!/bin/bash
DIR=test_merge
rm -rf $DIR
mkdir $DIR
cd $DIR
git init
echo "#include <stdio.h>" > hello.c
git add -f hello.c
git commit -m "Initial commit"
git checkout -b helloGit
echo "#include <stdlib.h>" > hello.c
git add -f hello.c
git commit -m "Update from helloGit branch"
git checkout master
echo "#include <string.h>" > hello.c
git add -f hello.c
git commit -m "Update from master"
git merge helloGit
