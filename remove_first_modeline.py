#!/usr/bin/env python2
from os import path
from sys import argv, exit
import logging

TO_REMOVE = ["# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1-unix -*-",
             "# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1 -*-"]
# TO_REMOVE = "# -*-"
EXTENSION = ".py"

if len(argv) < 2:
    print("no path given")


top_dir = argv[1]


def remove_comment(arg, dirname, fnames):
    # we can do some smart filtering based on the extension
    def rewrite_if_matching(fname):
        lines = open(fname).readlines()

        if lines: print(lines[0])
        if lines and lines[0] in TO_REMOVE:
            print("removing from %s line %s" % (fname, lines[0]))
            # open(fname, 'w').writelines(lines[1:])

    for f in fnames:
        if f.endswith(EXTENSION)
        full = path.join(dirname, f)
        #  FIXME: why do I need to check if it's a file
        if path.isfile(full):
            rewrite_if_matching(full)

path.walk(top_dir, remove_comment, None)
