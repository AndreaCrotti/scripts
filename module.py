#!/usr/bin/env python2

import argparse
from ast import parse
from os import walk, path
from sys import argv

def simple(module_path):
    return open(module_path).read()


class Module(object):
    def __init__(self, module_path):
        self.module_path = module_path
        self.text = None
        self.ast = None

    def get_text(self):
        if not self.text:
            self.text = open(self.module_path).read()
        return self.text

    def get_ast(self):
        self.get_text()
        if not self.ast:
            self.ast = parse(self.text)


class ContentDirectory(object):
    def __init__(self):
        self.content = {}

    def __getitem__(self, module_path):
        if module_path not in self.content:
            self.content[module_path] = Module(module_path)

        return self.content[module_path]


def show_content(dirpath, cd, cached):
    for root, _, files in walk(dirpath):
        for f in files:
            if f.endswith('.py'):
                full = path.join(root, f)
                if cached:
                    cd[full].get_text()
                else:
                    simple(full)


def parse_arguments():
    parser = argparse.ArgumentParser(description='test some caching')
    parser.add_argument('-c', '--cached',
                        action='store_true',
                        help='cached')
    parser.add_argument('dir')
    parser.add_argument('-n', '--number', default=10)

    return parser.parse_args()


if __name__ == '__main__':
    content_dir = ContentDirectory()
    ns = parse_arguments()
    for i in range(int(ns.number)):
        show_content(ns.dir, content_dir, ns.cached)
