#!/usr/bin/env python2
from os import path
from sys import argv, exit
import logging
import argparse

TO_REMOVE = ["# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1-unix -*-",
             "# -*-mode: python; py-indent-offset: 4; tab-width: 8; coding: iso-8859-1 -*-"]

DEFAULT_EXTENSION = ".py"

def remove_comment(arg, dirname, fnames, modify=False):
    # we can do some smart filtering based on the extension
    def rewrite_if_matching(fname):
        lines = open(fname).readlines()

        if lines: print(lines[0])
        if lines and lines[0] in TO_REMOVE:
            print("removing from %s line %s" % (fname, lines[0]))
            if modify:
                print("really modifying things")
                # open(fname, 'w').writelines(lines[1:])

    for f in fnames:
        if f.endswith(EXTENSION):
            full = path.join(dirname, f)
            #  FIXME: why do I need to check if it's a file
            if path.isfile(full):
                rewrite_if_matching(full)

# path.walk(top_dir, remove_comment, None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PSI cleanup script')

    parser.add_argument('-n', '--simulate', action='store_false')
    # this should be of type string
    parser.add_argument('-r', '--regexp')
    parser.add_argument('-d', '--dest', nargs='+')
    parser.add_argument('-e', '--ext', default=DEFAULT_EXTENSION)

    parser.parse_args(argv)
