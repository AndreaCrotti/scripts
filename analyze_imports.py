#!/usr/bin/env python2

import argparse

from ast import parse, NodeVisitor
from os import path
from pprint import pprint

from psi.devsonly.walk import walk_py, walk_full_path_files


class ImportVisitor(NodeVisitor):

    def __init__(self):
        self.imported = set()
        super(ImportVisitor, self).__init__()

    def __str__(self):
        return '\n'.join(x for x in self.imported)

    #TODO: maybe I should make a difference between these two cases?
    def visit_Import(self, node):
        for n in node.names:
            self.imported.add(n.name)

    #TODO: store something more than simply the name of the module
    #that we are using
    def visit_ImportFrom(self, node):
        self.imported.add(node.module)


def gen_module_imports(mod):
    try:
        at = parse(open(mod).read())
    except SyntaxError:
        print("file %s has a syntax error, please fix it" % mod)
        return []
    else:
        v = ImportVisitor()
        v.visit(at)
        return v.imported


def parse_arguments():
    parser = argparse.ArgumentParser(description='analyze the imports and print them out')
    # we can get a list of directories, files, or mix
    parser.add_argument('cont', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    ns = parse_arguments()
    imports = {}

    for cn in ns.cont:
        if path.isfile(path.abspath(cn)):
            imports[cn] = gen_module_imports(cn)

        elif path.isdir(path.abspath(cn)):
            for mod in walk_full_path_files(cn, walk_py):
                imports[mod] = gen_module_imports(mod)

    pprint(imports)
