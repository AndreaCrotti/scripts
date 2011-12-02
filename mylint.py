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

# done until now:
# - imports.py
# - variables.py

# associate every error we want to analyze with something
error_level = {
    WARNING: [
        ('W0611', 'unused_imports'),
        ('W0612', 'unused_variable'),
        ('W0613', 'unused_argument'),
        ('R0401', 'cyclic_import'),
        ('W0401', 'star_import'),  #  this might be an error too
        ('W0403', 'relative_import'),
        ('W0404', 'double_import'),
    ],
    ERROR: [
        ('E0104', 'return_outside_function'),
        ('E0105', 'yield_outside_function'),
        ('E0602', 'name_not_found'),
        ('E0601', 'variable_before_assignment'),
        ('W0410', 'future_not_first')
    ],
    # what could be some fatal?
    FATAL: [

    ]
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
