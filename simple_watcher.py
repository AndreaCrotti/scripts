#!/usr/bin/env python2
"""
Simple way to watch for changes

Doesn't cope with moved files and doesn't scale so well, but not as
bad as it looks
"""

import os
import time
import sys

path_to_watch = sys.argv[1]
before = dict([(f, None) for f in os.listdir(path_to_watch)])

while True:
    time.sleep(5)
    after = dict([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: print "Added: ", ", ".join(added)
    if removed: print "Removed: ", ", ".join(removed)
    before = after
