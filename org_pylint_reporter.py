#!/usr/bin/env python

import sys
import argparse
from os import path

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from logilab.common.ureports import TextWriter


class OrgReporter(BaseReporter):
    __implements__ = IReporter

    extension = 'org'

    def __init__(self, output=sys.stdout):
        #XXX: this is because the base class is old-style, and the usual super doesn't work
        BaseReporter.__init__(self, output)
        # the col_offset is also important to identify the problem

    # we can even use the line content in theory to make it more precise
    def _orgmode_line(self, module, msg_id, line):
        full_path = path.abspath("%s.py" % module)
        link = "[[file:%s::%d][%s]]" % (full_path, line, module)
        return "* TODO %s     :%s:" % (link, msg_id)

    def add_message(self, msg_id, location, msg):
        module, obj, line, col_offset = location[1:]
        self.writeln(self._orgmode_line(module, msg_id, line))

    def _display(self, layout):
        print >> self.out
        TextWriter().format(layout, self.out)


def pylint_cmdline(module):
    msg_ids = get_msg_ids(error_level)
    msgs = ','.join(msg_ids)
    to_disable = 'I,W,R,C,E'
    options = "-i y -rn -d %s -e %s %s" % (msgs, to_disable, module)
    options = options.split(' ')
    print("running %s" % (str(options)))
    # needs to pass the reporter object too
    Run(options, reporter=OrgReporter())