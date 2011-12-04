#!/usr/bin/env python2
"""
Generate flow-charts from real working python code.  The syntax needs
to be a lot simplified, but it should be parsed by a simple AST parser
and produce a graph which can be shown with networkx.

if x > 0:
    do something

else:
    something else

# what is below this if-else should be son of both things
# another supposition is that everything should fit in one line
"""

import networkx as nx
import matplotlib.pyplot as plt
import ast
import argparse
import sys


class FlowchartVisitor(ast.NodeVisitor):
    def __init__(self, text):
        self.graph = nx.graph.Graph()
        self.text = text.splitlines()

    def visit_If(self, node):
        if_test = node.test
        comparison = self.text[if_test.lineno-1][if_test.col_offset:]
        if_str = "if %s" % comparison
        # whenever I have an if I create a conjunction
        if_node = self.graph.add_node(if_str)

    def draw_graph(self, output='graph.png'):
        plt.clf()
        plt.grid(False)
        print("generating graph to %s" % output)
        pos = nx.layout.random_layout(self.graph)
        nx.draw_networkx_nodes(self.graph,
                               pos=pos,
                               node_color='white')
        # not storing anything like this
        plt.savefig(output)


def gen_flowchart(source):
    try:
        mod = ast.parse(source)
    except SyntaxError:
        print("your code doesn't parse, try again")
        sys.exit(1)
    else:
        ast.fix_missing_locations(mod)
        v = FlowchartVisitor(source)
        v.visit(mod)
        v.draw_graph()


# there should be an "nx" class which can take care of generating
# objects in the right position, and link them accordingly

def parse_arguments():
    parser = argparse.ArgumentParser(description='Given the input text creates a nice flowchart')

    parser.add_argument('-o', '--output', help='output file')
    # if not set maybe it should take the standard input
    parser.add_argument('input_file',
                        help='input file',
                        nargs='?')
    return parser.parse_args()


def main():
    ns = parse_arguments()
    if not ns.input_file:
        inp = sys.stdin.read()
    else:
        inp = open(ns.input_file).read()

    gen_flowchart(inp)

if __name__ == '__main__':
    main()
