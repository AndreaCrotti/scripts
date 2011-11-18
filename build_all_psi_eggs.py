#!/home/andrea/python_pack/airbus_epd-2.5.2001.b1-rh3_amd64/bin/python
"""
Build all the PSI eggs with develop or bdist_egg depending on the case
"""

from os import getenv, path, mkdir
from subprocess import Popen, PIPE
from glob import glob
# add also this to the third party as egg
import argparse

PSI_PATH = path.expanduser("~/workspace/Psi")
# PSI_PATH = getenv("PSI_PATH")
BASE_ENV_PATH = path.expanduser(path.join('~', '.virtualenvs'))
EGG_DIR = path.expanduser(path.join('~', '.psi_eggs'))
# where is the server running
PYTHON_CMD = "python"

# glob on the paths without using chdir, but using the absolute paths

# use os.walk to scan through the needed eggs, to rebuild them
# automatically

def initialise():
    if not path.exists(EGG_DIR):
        # make sure that the destination directory actually exists
        mkdir(EGG_DIR)

# TODO: just create the bdist_egg and make sure that the local pypi
# server is actually running, then "develop" will actually be easier
# to solve
def analyzer(option):
    # get the return value with subprocess
    eggs = glob(path.join(PSI_PATH, '*'))
    if option == 'list':
        print(str(eggs))
        return

    print("going to actually build all the eggs")
    initialise()
    # it's more simple to use GLOB and similar things
    cmd = "%s setup.py %s" % (PYTHON_CMD, option)
    while eggs:
        egg = eggs.pop()
        # TODO: filter in a smarter way possibly
        if not path.exists(path.join(egg, "setup.py")):
            print("filtering out egg %s" % egg)
            continue

        # check if you really need it and how
        print("building egg %s" % egg)
        # change the directory before running
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=egg)
        out, err = p.communicate()

        # TODO: make it as parallel as possible
        if p.returncode != 0:
            print("setup on %s failed, add it again to the list" % egg)
            eggs.insert(0, egg)
            print(err)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='script to run things')
    parser.add_argument('-b', '--build',
                        help='build the binary eggs',
                        action='store_true')

    parser.add_argument('-l', '--list', action='store_true')
    #TODO: make sure we do either one or the other one
    ns = parser.parse_args()

    if ns.build:
        option = 'bdist_egg -d %s' % EGG_DIR
    else:
        print("only showing the given eggs")
        option = 'list'

    analyzer(option)
