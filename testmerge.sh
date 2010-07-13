#!/bin/bash
git init
echo Hello World! > hello.txt
git add hello.txt
git commit -m "Initial commit"
git checkout -b helloGit
echo Hello Git! > hello.txt
git add hello.txt
git commit -m "Update from helloGit branch"
git checkout master
echo Hello World! Hello indeed! > hello.txt
git add hello.txt
git commit -m "Update from master"
git merge helloGit
