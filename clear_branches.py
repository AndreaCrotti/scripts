#!/usr/bin/env python2.7

import sys
import git

if len(sys.argv) != 2:
    print("Need to pass the path argument")
    sys.exit(1)

repo = git.Repo(sys.argv[1])

to_keep = ['staging', 'master', 'dev', 'trycollectfast']

for branch in repo.branches:
    name = branch.name
    if not any(name in tok for tok in to_keep):
        print("deleting branch {}".format(name))
        repo.delete_head(name, force=True)
