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

    def __setattribute__(self, attr, value):
        self.cmd.append((attr, value))

    def add(self, attr):
        self.cmd.append(attr)

    def execute(self):
        # TODO: check the return code and parallelize when possible 
        subprocess.Popen(str(self), shell=True)


class RdiffCommand(ShellCommand):
    " Rdiff commands"
    def __init__(self, base=HOME):
        # a command is a list of options, arguments etc etc
        super(RdiffCommand, self).__init__(base)
        self.cmd.append(CMD % "rdiff-backup")

    def exclude_list(self, exts):
        return '|'.join([x + '$' for x in exts])


class GitCommand(ShellCommand):
    def __init__(self, base=HOME, repo=None):
        super(GitCommand, self).__init__(base)
        # if the destination file already exists we should use git pull instead, much faster
        self.repo = repo.split("/")[-1]

    def execute(self, dest):
        from os import listdir, getcwd
        chdir(dest)
        if path.exists(self.repo):
            chdir(self.repo)
            self.add(CMD % "git pull")
        else:
            self.add(CMD % ("git clone %s" % self.repo))

        super(GitCommand, self).execute()


def backup(dest):
    # keep a list to make them run in parallel as much as possible
    commands = []
    # read the configuration how to do it
    for s in conf['sources']:
        if isinstance(s, dict):
            # then look inside the list, must also add those items
            # to the exclude list for the corresponding
            subkey = s.keys()[0]
            for subdir, repo in s[subkey].items():
                if repo == 'git':
                    gt = GitCommand(repo=subdir)
                    commands.append(gt)

        # elif isinstance(s, str):
        #     # pass the right verbosity flags and so on
        #     rd = RdiffCommand()
        #     # depending on the type of connection we should do different things
        #     # rd += 
        #     # now add the right arguments
        #     commands.append(rd)

    for cmd in commands:
        # print cmd
        cmd.execute(conf['destinations'][dest]['path'])


if __name__ == '__main__':
    opts, args = getopt('vd:', argv[1:])
    glob_verbose = False

    destination = None

    for o, a in opts:
        if '-v' in o:
            glob_verbose = True
        if '-d' in o:
            destination = a

    # assert(destination is not None)

    backup('test')
    
