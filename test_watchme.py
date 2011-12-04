import sys
import time
import argparse

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

import logging

# - a FileDeleted event should trigger a check for pesky .pyc files
# - a FileModified event on a setup.py or a c library should instead trigger a rebuild-redevelop
# - should I use only on thread or multiple threads to check all the different things?


class HandlePeskyPycFiles(LoggingEventHandler):
    def on_moved(self, event):
        super(HandlePeskyPycFiles, self).on_moved(event)
        if not event.is_directory:
            # then it must be a file
            if event.src_path.endswith('.py'):
                print("moving a python file, must check for pyc")
            else:
                print("file moved was not a pyc, go on")


def parse_arguments():
    parser = argparse.ArgumentParser(description='testing watchdog')
    parser.add_argument('dir')

    return parser.parse_args()

if __name__ == "__main__":
    ns = parse_arguments()

    event_handler = HandlePeskyPycFiles()
    observer = Observer()
    observer.schedule(event_handler, ns.path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
