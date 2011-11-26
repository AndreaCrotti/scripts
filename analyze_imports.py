#!/usr/bin/env python2

import argparse

from ast import parse, NodeVisitor


class ImportVisitor(NodeVisitor):

    def __init__(self):
        self.imported = set()
        super(ImportVisitor, self).__init__()

    def __str__(self):
        return str(self.imported)        

    #TODO: maybe I should make a difference between these two cases?
    def visit_Import(self, node):
        for n in node.names:
            self.imported.add(n.name)

    def visit_ImportFrom(self, node):
        self.imported.add(node.module)


def show_imports(mod):
    at = parse(open(mod).read())
    v = ImportVisitor()
    v.visit(at)
    print v


def parse_arguments():
    parser = argparse.ArgumentParser(description='analyze the imports and print them out')
    
    parser.add_argument('modules', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    ns = parse_arguments()
    for mod in ns.modules:
        show_imports(mod)
