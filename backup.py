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
from os import path, chdir
from getopt import getopt
from sys import argv

conf = yaml.load(open("backup.yaml"))

# should only generate one huge rsync command

HOME = path.expanduser("~")
CMD  = "env %s"

# TODO: add a check to make sure that the address really exists 
class ShellCommand(object):
    def __init__(self, base):
        # base path for the command, also from where it should be executed
        self.base = base
        self.cmd = []

    def __str__(self):
        return " ".join(self.cmd)

    def execute(self):
        chdir(self.base)
    

class RdiffCommand(ShellCommand):
    " Rdiff commands"
    def __init__(self, verbose=False, base=HOME):
        # a command is a list of options, arguments etc etc
        super(RdiffCommand, self).__init__(base)
        self.cmd.append(CMD % "rdiff-backup")
        if verbose:
            self.cmd.append("-v")

    def __setattribute__(self, attr, value):
        self.cmd.append((attr, value))

    def __add__(self, attr):
        self.cmd.append(attr)

class GitCommand(ShellCommand):
    def __init__(self, verbose=False, base=HOME):
        self.cmd.append("git clone")
        if self.verbose:
            self.cmd.append("-v")

if __name__ == '__main__':
    opts, args = getopt('v', argv[1:])
    glob_verbose = False
    for o, a in opts:
        if '-v' in o:
            glob_verbose = True

    print conf
    rs = RdiffCommand()
    print rs
    
