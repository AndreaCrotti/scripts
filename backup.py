#!/usr/bin/env python
import yaml

"""
Two main possible destination type
- backup disk
- other host

rsync can be used in both cases unless the destination disk is in fat32.
for saving some space we can use git clone whenever we are backing up a git repository
"""

conf = yaml.load(open("backup.yaml"))

if __name__ == '__main__':
    print conf
