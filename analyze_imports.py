#!/usr/bin/env python2

import argparse

from compiler import parseFile
from compiler.visitor import ASTVisitor

# now we can define a visitor

def show_imports(mod):
    ast = parseFile(mod)
    for n in ast.node.nodes:
        print(n)


def parse_arguments():
    parser = argparse.ArgumentParser(description='analyze the imports and print them out')
    
    parser.add_argument('modules', nargs='+')
    return parser.parse_args()


if __name__ == '__main__':
    ns = parse_arguments()
    for mod in ns.modules:
        show_imports(mod)
