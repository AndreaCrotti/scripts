#!/usr/bin/env python2
from os import path, exists
from sys import argv, exit
import logging

TO_REMOVE="# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1-unix -*-"

if len(argv) < 2:
    print("no path given")


top_dir = argv[1]

def remove_comment(arg, dirnames, fnames):
    # we can do some smart filtering based on the extension
    def rewrite_if_matching(fname):
        # TODO: check lazily that the file is actually changed with the timestamp
        # or more simpler just use a find to get the number of the line also
        filtered = (l for l in file(fname) if l != TO_REMOVE)
        file(fname, 'w').writelines(filtered)

        # return number of line and 

    for f in fnames:
        pass
