#!/usr/bin/env python2

from ast import parse
from os import walk, path
from sys import argv


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


def show_content(dirpath, cd):
    for root, _, files in walk(dirpath):
        for f in files:
            if f.endswith('.py'):
                full = path.join(root, f)
                cd[full].get_text()


if __name__ == '__main__':
    content_dir = ContentDirectory()
    for i in range(int(argv[2])):
        show_content(argv[1], content_dir)
