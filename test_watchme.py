#!/usr/bin/env python2
import sys
import time
import argparse

from os import path, remove

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import logging

# - a FileDeleted event should trigger a check for pesky .pyc files
# - a FileModified event on a setup.py or a c library should instead trigger a rebuild-redevelop
# - should I use only on thread or multiple threads to check all the different things?

# possible workflow
# - when dev_main starts:
#  + if watchme daemon is found runs very smoothly
#  + otherwise try to start it and if it starts correctly use it
#  + otherwise record that it doesn't work on the current machine and stop it
#
# Moreover, it might be nice to record somewhere a transaction system,
# to avoid repeating the same develop if it didn't fail the time
# before.  Might need 2 C-c to quit completely, where the first one
# falls in a pdb debugger modality.


class HandlePeskyPycFiles(LoggingEventHandler):
    def _is_py_module(self, filename):
        #TODO: check also if it's a filename somehow, but this file is
        #already the old path, so we can't really check for path.isfile
        return filename.endswith('.py')

    def _check_and_delete_pesky(self, py_module):
        assert not path.isfile(py_module)
        print("checking pesky")
        pyc_file = py_module + "c"
        if path.isfile(pyc_file):
            print("removing pesky file")
            remove(pyc_file)

    def on_deleted(self, event):
        super(HandlePeskyPycFiles, self).on_deleted(event)
        #XXX: slight repetition of things, but more flexible in this way
        if self._is_py_module(event.src_path):
            self._check_and_delete_pesky(event.src_path)

    # the other functions should be checked
    def on_moved(self, event):
        super(HandlePeskyPycFiles, self).on_moved(event)
        if self._is_py_module(event.src_path):
            self._check_and_delete_pesky(event.src_path)


def parse_arguments():
    parser = argparse.ArgumentParser(description='testing watchdog')
    parser.add_argument('dir')

    return parser.parse_args()

if __name__ == "__main__":
    ns = parse_arguments()

    event_handler = HandlePeskyPycFiles()
    observer = Observer()
    observer.schedule(event_handler, ns.dir, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
