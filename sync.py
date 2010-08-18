#!/usr/bin/env python
# Time-stamp: <18-08-2010, 23:46>
# TODO: put all the single files together in only one sync

import os
#import logging
#import subprocess
#import smtplib # necessary for sending mails with the errors

from optparse import OptionParser
from sys import exit

HOME = os.path.expanduser("~")

RSYNC = "/usr/bin/env rsync"
GIT = "/usr/bin/env git"
# FIXME: those globals are really bad
EXCLUDE = os.path.expanduser("~/bin/exclude_list")
RSYNC_OPTIONS = " --exclude-from=" + EXCLUDE + " -az --relative"
FILES = os.path.expanduser("~/bin/files.txt")

# only pretending for now
RSYNC_CMD = RSYNC + RSYNC_OPTIONS + "  %s %s"
GIT_CMD = "cd %s && " + GIT + " push -n %s master"
DST = "%s:%s"


def sync_files(host):
    "Synchronizes files to destination"
    os.chdir(HOME)
    for f in open(FILES):
        if "#" in f:
            continue
        dst = DST % (host, f)
        if os.path.exists(os.path.join(f, ".git")):
            # then is a git repository!
            cmd = GIT_CMD % (f, dst)
        else:
            cmd = RSYNC_CMD % (f, dst)

        print "running command %s" % cmd
        _, out = os.popen2(cmd)
        print out.read()

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
    
