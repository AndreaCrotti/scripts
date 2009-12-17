#!/usr/bin/env python
# Time-stamp: <17-12-2009, 15:20>

import os
#import logging
from optparse import OptionParser
from sys import exit

HOME = os.path.expanduser("~")

RSYNC = "/usr/bin/env rsync"
# TODO: make it more general
FILES = open('files.txt').read().split('\n')[:-1]

EXCLUDE = os.path.expanduser("~/bin/exclude_list")
OPTIONS = ["--exclude-from=" + EXCLUDE, "-az", "--relative"]

CMD = RSYNC + " %(opts)s %(src)s %(dst)s"

def sync_files(dst, confirm = False):
    "Synchronize the file calling rsync with the global OPTIONS"
    os.chdir(HOME)
    dic = {}
    for f in FILES:
        dic[f] = []
        if os.path.isdir(f):
            dic[f].append("--delete-after")
    for d in dic.iterkeys():
        cmd = CMD % {'opts' : ' '.join(OPTIONS + dic[d]),
                     'src' : d, 'dst' : dst + ":"}
        if not(confirm):
            while True:
                r = raw_input("executing %s, confirm? y/n\n" % cmd)
                if r == 'y':
                    break
                elif r == 'n':
                    exit(0)
        _, output = os.popen2(cmd)
        print output.read()

if __name__ == '__main__':
    # FIXME: not really nice use of global
    global OPTIONS
    opt_parser = OptionParser(usage = "push_data.py -o <additional options> [-p] user@host")
    opt_parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose")
    opt_parser.add_option("-p", "--pretend", action = "store_true", dest = "pretend",
                          help = "just pretend don't do")
    opt_parser.add_option("-y", "--no-confirm", action = "store_true",
                          dest = "confirm", help = "don't demand confirmation")
    (options, args) = opt_parser.parse_args()

    if options.pretend:
        OPTIONS.append("-n")
        
    if options.verbose:
        OPTIONS.append("-v")
        
    # using the correct 
    if not args:
        exit(os.EX_NOINPUT)
    
    # this can also send on more hosts at the same time!
    # maybe should be better if running in parallel?
    for host in args:
        sync_files(host, confirm = options.confirm)
    
