#!/usr/bin/env python
# TODO: put all the single files together in only one sync
# TODO: fix the ssh keys problem with mini
# TODO: make it recursively analyzing if there are .git directories inside it
# TODO: pushing to a normal git repo doesn't work, or pull from it via ssh or create some bare repos

import os, sys
#import logging
import subprocess

from optparse import OptionParser
from sys import exit

HOME = os.path.expanduser("~")

RSYNC = "/usr/bin/env rsync"
GIT = "/usr/bin/env git"
# FIXME: those globals are really bad
EXCLUDE = os.path.expanduser("~/bin/exclude_list")
RSYNC_OPTIONS = " --exclude-from=" + EXCLUDE + " -azv --relative"
FILES = os.path.expanduser("~/bin/files.txt")

# only pretending for now
RSYNC_CMD = RSYNC + RSYNC_OPTIONS + " %s %s"
GIT_CMD = "cd %s && " + GIT + " push -n %s master"

def sync_files(host):
    "Synchronizes files to destination"
    os.chdir(HOME)
    for f in open(FILES):
        # TODO: use a more general way to parse and strip 
        if "#" in f:
            continue
        f = f.strip()
        if os.path.exists(os.path.join(f, ".git")):
            # then is a git repository!
            cmd = GIT_CMD % (f, "%s:%s" % (host, f))
            # FIXME: not working yet
            continue
        else:
            cmd = RSYNC_CMD % (f, "%s:" % host)

        print "running command %s" % cmd
        # FIXME: this is really a bad idea
        os.system(cmd)
        # subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)

if __name__ == '__main__':
    # TODO: make it looks nicer 
    opt_parser = OptionParser(usage = "push_data.py -o <additional options> [-p] user@host")
    opt_parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose")
    opt_parser.add_option("-p", "--pretend", action = "store_true", dest = "pretend",
                          help = "just pretend don't do")

    (opts, args) = opt_parser.parse_args()

    options = ["--exclude-from=" + EXCLUDE, "-az", "--relative"]


    if opts.pretend:
        options.append("-n")
        
    if opts.verbose:
        options.append("-v")
        
    # using the correct 
    if not args:
        exit(os.EX_NOINPUT)
    
    # TODO: make it able to run in parallel
    # this can also send on more hosts at the same time!
    # maybe should be better if running in parallel?
    for host in args:
        sync_files(host)
