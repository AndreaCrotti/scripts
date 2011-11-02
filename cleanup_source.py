#!/usr/bin/env python2
from os import path
from sys import argv, exit
import logging
import argparse

#TODO: remove empty newlines after this too
TO_REMOVE = "# -*-mode: python"
EXTENSION = ".py"
SIMULATE = False

# TODO: make TO_REMOVE also a parameter
def remove_comment(arg, dirname, fnames):
    # we can do some smart filtering based on the extension
    def rewrite_if_matching(fname):
        lines = open(fname).readlines()

        if lines and lines[0].startswith(TO_REMOVE):
            print("removing from %s line %s" % (fname, lines[0]))

            if not SIMULATE:
                print("really modifying things")
                open(fname, 'w').writelines(lines[1:])

    for f in fnames:
        if f.endswith(EXTENSION):
            full = path.join(dirname, f)
            #  FIXME: why do I need to check if it's a file
            if path.isfile(full):
                rewrite_if_matching(full)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PSI cleanup script')

    parser.add_argument('-n', '--simulate', action='store_true')
    # this should be of type string
    parser.add_argument('-r', '--regexp')
    parser.add_argument('dest', nargs='+')
    parser.add_argument('-e', '--ext')

    args = parser.parse_args()

    import pdb; pdb.set_trace()
    #TODO: check why the simulate is not actually followed correctly
    if args.simulate:
        global SIMULATE
        SIMULATE = True

    if args.ext:
        global EXTENSION
        EXTENSION = True

    if args.regexp:
        global TO_REMOVE
        TO_REMOVE = args.regexp

    for d in args.dest:
        path.walk(d, remove_comment, None)
