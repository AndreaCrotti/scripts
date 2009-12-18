#!/usr/bin/env python
# Time-stamp: <18-12-2009, 13:40>
# TODO: put all the single files together in only one sync

import os
#import logging
#import subprocess

from optparse import OptionParser
from sys import exit, stdout

HOME = os.path.expanduser("~")

RSYNC = "/usr/bin/env rsync"
# TODO: make it more general
EXCLUDE = os.path.expanduser("~/bin/exclude_list")
FILES = os.path.expanduser("~/bin/files.txt")

FILELIST = open(FILES).read().split('\n')[:-1]

CMD = RSYNC + " %(opts)s %(src)s %(dst)s"

def sync_files(dst, options, confirm = True):
    "Synchronize the file calling rsync with the global OPTIONS"
    os.chdir(HOME)
    dic = {}
    for f in FILELIST:
        dic[f] = []
        if os.path.isdir(f):
            dic[f].append("--delete-after")
    for d in dic.iterkeys():
        cmd = CMD % {'opts' : ' '.join(options + dic[d]),
                     'src' : d, 'dst' : dst + ":"}
        sync = True
        if confirm:
            r = raw_input("executing %s, confirm? y/n\n" % cmd)
            if r != 'y':
                sync = False
                print "skipping %s from sync" % d

        if sync:
            print "running command %s" % cmd
        # by default is already going to stdout
        # TODO: make it possible to log somewhere the stderr
        _, out = os.popen2(cmd)
        print out.read()

if __name__ == '__main__':
    # FIXME: not really nice use of global
    opt_parser = OptionParser(usage = "push_data.py -o <additional options> [-p] user@host")
    opt_parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose")
    opt_parser.add_option("-p", "--pretend", action = "store_true", dest = "pretend",
                          help = "just pretend don't do")
    opt_parser.add_option("-y", "--no-confirm", action = "store_false",
                          dest = "confirm", help = "don't demand confirmation")
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
        sync_files(host, options, confirm = opts.confirm)
    
