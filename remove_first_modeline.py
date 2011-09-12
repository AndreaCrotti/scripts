#!/usr/bin/env python2
from os import path
from sys import argv, exit
import logging

TO_REMOVE="# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1-unix -*-"

if len(argv) < 2:
    print("no path given")


top_dir = argv[1]


def remove_comment(arg, dirname, fnames):
    # we can do some smart filtering based on the extension
    def rewrite_if_matching(fname):
        lines = open(fname).readlines()

        if lines and TO_REMOVE == lines[0].strip():
            print("removing from %s" % fname)
            file(fname, 'w').writelines(lines[1:])

    for f in fnames:
        full = path.join(dirname, f)
        #  FIXME: why do I need to check if it's a file
        if path.isfile(full):
            rewrite_if_matching(full)

path.walk(top_dir, remove_comment, None)
