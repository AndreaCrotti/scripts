#!/usr/bin/env python

"""
Two main possible destination type
- backup disk
- other host

rsync can be used in both cases unless the destination disk is in fat32.
for saving some space we can use git clone whenever we are backing up a git repository
"""

import yaml
import subprocess # for the call process

conf = yaml.load(open("backup.yaml"))

# should only generate one huge rsync command

HOME = os.path.expanduser("~")

class ShellCommand(object):
    def __init__(self, base=HOME, verbose=False):
        self.verbose = verbose
        # base path for the command, also from where it should be executed
        self.base = base

    def __str__(self):
        return " ".join(self.cmd)

    def execute(self):
        pass


class RsyncCommand(object):
    def __init__(self, verbose):
        # a command is a list of options, arguments etc etc
        self.cmd = []

    def __setattribute__(self, attr, value):
        self.cmd.append((attr, value))

if __name__ == '__main__':
    print conf
    RsyncCommand(cmd, base="/usr")
    
