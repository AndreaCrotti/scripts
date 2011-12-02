import argparse

from pylint.lint import PyLinter
from pylint.reporters import BaseReporter

from pylint.interfaces import IReporter

# possible levels
CRITICAL = 3
FATAL = CRITICAL
ERROR = 2
WARNING = 1
WARN = WARNING
STYLE = 0

# associate every error we want to analyze with something
error_level = {
}

class MyReporter(BaseReporter):
    def add_message(self, msg_id, location, msg):
        """add a message of a given type

        msg_id is a message identifier
        location is a 3-uple (module, object, line)
        msg is the actual message
        """

    # def display_results(self, layout):
    #     """display results encapsulated in the layout tree"""



def parse_arguments():
    parser = argparse.ArgumentParser(description='run pylint on the file')

    return parser.parse_args()
