#!/usr/bin/env python2

import sys
import argparse
from os import path

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter
from pylint.lint import Run

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


def run_pylint(module, output, msg_ids=None):
    if msg_ids:
        to_disable = 'I,W,R,C,E'
        enable_only = "-d %s -e %s" % (to_disable, ','.join(msg_ids))
    else:
        enable_only = ''

    options = "-i y -rn %s %s" % (enable_only, module)
    options = options.split(' ')
    Run(options, reporter=OrgReporter(output=output))


def parse_arguments():
    parser = argparse.ArgumentParser(description='run pylint and convert the output to orgmode format')

    parser.add_argument('-o', '--output')
    parser.add_argument('module')
    parser.add_argument('msg_id', nargs='*')

    return parser.parse_args()


if __name__ == '__main__':
    ns = parse_arguments()
    output = ns.output if ns.output else sys.stdout
    run_pylint(ns.module, output, ns.msg_id)
