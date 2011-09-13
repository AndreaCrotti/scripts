#!/usr/bin/env python

from sys import argv, exit
from os import path, mkdir, chdir
from shutil import copy

# creates the directory structure necessary
# Proj
# |_ airbus.proj
#    |_ setup.cfg
#    |_ setup.py
#    |_ airbus
#       |_ __init__.py
#       |_ proj_plugin.py
#       |_ test
#          |_ __init__.py

# missing the UI part

def usage():
    print("usage: %s project_name")
    exit(1)


if len(argv) < 2:
    usage()

NAME = argv[1]
SETUPS = [path.join("templates", "setup." % x) for x in ("cfg", "py")]

def make_dir_safe(path):
    # TODO: also check that there isn't already a directory
    if not path.exists(path):
        mkdir(path)
    else:
        assert(path.isdir(path))

make_dir_safe(NAME)
chdir(NAME)

# TODO: uncamelize the name if possible
SUBDIR = "airbus.%s" % NAME
make_dir_safe(SUBDIR)

# where should it fetch the
for set_file in SETUPS:
    copy(set_file, SUBDIR)
    

chdir(SUBDIR)

