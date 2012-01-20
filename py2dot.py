# original code from http://pypi.python.org/pypi/py2dot
"""Create a dot file from a Python file.

Read a Python files and create a dot file of the function used and called.
Imported modules are scanned too, up to a user-defined level of recursion.
The dot file can be viewed with Graphviz.

The basic usage is:

$> ./py2dot -f filename.py | dot -Tpng | display

For command line options, type:

$> ./py2dot -h

Inside a Python shell:

>>> import py2dot
>>> infile = open('test.py', 'r')
>>> reclevel = 1
>>> data = py2dot.FileInput(infile, maxreclevel=reclevel)
>>> print data

"""

__author__ = 'Lorenzo Bolla'

import sys
import os.path
import parser
import symbol
import token
from pprint import pprint
from optparse import OptionParser

class HashableName:
    """Class to redefine the hash function. Used for user-defined data types that must go into sets."""
    def __hash__(self):
        return self.name.__hash__()
    def __eq__(self, x):
        return self.name == x.name

class Element:
    """A generic element of the parsing tree."""
    def validate(self, ast):
        if ast[0] != self.sym_code:
            raise ValueError('%d != %d' % (ast[0], self.sym_code))

class DottedName(Element, HashableName):
    sym_code = symbol.dotted_name

    def parse(self, ast):
        self.validate(ast)
        name = ''
        for item in ast[1:]:
            name += item[1]
        self.name = name
        return self

    def __str__(self):
        return self.name

class DottedAsName(Element, HashableName):
    sym_code = symbol.dotted_as_name

    def parse(self, ast):
        self.validate(ast)
        dn = DottedName().parse(ast[1])
        self.name = dn.name
        return self

    def __str__(self):
        return self.name

class DottedAsNames(Element, set):
    sym_code = symbol.dotted_as_names

    def parse(self, ast):
        self.validate(ast)
        for item in ast[1::2]:
            das = DottedAsName().parse(item)
            self.add(das)
        return self

class ImportFrom(Element, set):
    sym_code = symbol.import_from

    def parse(self, ast):
        self.validate(ast)
        for item in ast[1:]:
            try:
                dn = DottedName().parse(item)
                self.add(dn)
            except:
                continue
        return self

class ImportName(Element, set):
    sym_code = symbol.import_name

    def parse(self, ast):
        self.validate(ast)
        self.update(DottedAsNames().parse(ast[2]))
        return self

class FuncDef(Element, HashableName):
    sym_code = symbol.funcdef

    def parse(self, ast):
        self.validate(ast)
        self.name = ast[2][1]
        fc_set = set()
        recapply(ast[5], FuncCall, fc_set)
        self.calls = fc_set
        return self

class Atom(Element, HashableName):
    sym_code = symbol.atom

    def parse(self, ast):
        self.validate(ast)
        if ast[1][0] != token.NAME:
            raise ValueError()
        self.name = ast[1][1]
        return self

class FuncCall(Element, HashableName):
    sym_code = symbol.power

    def parse(self, ast):
        global COMPLETE_NAME
        self.validate(ast)
        # 'return' statement have no parameters
        if len(ast) < 3:
            raise ValueError()
        self.name = Atom().parse(ast[1]).name
        for item in ast[2:]:
            if item[1][0] == token.DOT:
                # call with full module path
                if COMPLETE_NAME:
                    self.name = make_name(self.name, item[2][1])
                else:
                    # only function name
                    self.name = item[2][1]
        return self

class ClassDef(Element, HashableName):
    sym_code = symbol.classdef

    def parse(self, ast):
        global COMPLETE_NAME
        self.validate(ast)
        if ast[2][0] != token.NAME:
            raise ValueError()
        self.name = ast[2][1]
        cl_set = set()
        for a in ast[4:]:
            recapply(a, ClassDef, cl_set)
        self.classes = cl_set
        fn_set = set()
        for a in ast[4:]:
            recapply(a, FuncDef, fn_set)
        self.funcalls = fn_set
#        # OKKIO
#        if COMPLETE_NAME:
#            for fn in self.funcalls:
#                fn.name = make_name(self.name, fn.name)
#                for fc in fn.calls:
#                    fc.name = make_name(self.name, fc.name)
        return self

    def relationships(self):
        dot = ''
        for fn in self.funcalls:
            for fc in fn.calls:
                dot += line('%s -> %s;' % (fn.name, fc.name))
        for cl in self.classes:
            dot += cl.relationships()
        return dot

    def definitions(self):
        dot = ''
        dot += line('subgraph cluster_%s {' % self.name)
        dot += line('label = "%s";' % self.name)
        dot += line('style = dashed;')
        for fn in self.funcalls:
            dot += line('%s;' % fn.name)
        for cl in self.classes:
            dot += cl.definitions()
        dot += line('}')
        return dot

    def todotlist(self):
        dot = []
        # fun def inside a cluster
        dot.extend(self.definitions())
        # fun calls outside the cluster
        dot.extend(self.relationships())
        return dot

class FileInput(Element, HashableName):
    sym_code = symbol.file_input

    def __init__(self, filename, reclevel=0, maxreclevel=0):
        self.reclevel = reclevel
        self.maxreclevel = maxreclevel
        if reclevel > maxreclevel:
            raise ValueError()
        self.funcalls = set()
        self.classes = set()
        self.imports = set()
        self.file = filename
        self.name = os.path.basename(self.file.name).split('.')[0]
        code = self.file.read()

        ast = parser.suite(code)
        self.parse(ast.tolist())

    def parse(self, ast):
        global COMPLETE_NAME
        global EXCLUDE_CLASSES

        self.validate(ast)

        # classes
        cl_set = set()
        if not EXCLUDE_CLASSES:
            recapply(ast, ClassDef, cl_set)
        self.classes.update(cl_set)

        # function calls
        fn_set = set()
        recapply(ast, FuncDef, fn_set)
        self.funcalls.update(fn_set)

        # imports
        import_set = set()
        recapply(ast, ImportName, import_set)
        recapply(ast, ImportFrom, import_set)

        path = [os.path.dirname(self.file.name)] + sys.path
        for im in import_set:
            for p in path:
                try:
                    tmpfile = os.path.join(p, im.name + '.py')
                    data = FileInput(open(tmpfile, 'r'),
                            reclevel=self.reclevel+1,
                            maxreclevel=self.maxreclevel)
                    if COMPLETE_NAME:
                        for fn in data.funcalls:
                            fn.name = make_name(im.name, fn.name)
                            for fc in fn.calls:
                                fc.name = make_name(im.name, fc.name)
                    self.imports.add(data)
                except Exception, e:
                    pass

        return self

    def definitions(self, subgraph=False):
        dot = ''
        dot += line('/* definitions */')
        if subgraph:
            dot += line('subgraph cluster_%s {' % self.name)
            dot += line('style = filled; fillcolor = lightgrey;')
        dot += line('label = "%s";' % self.name)
        dot += line('splines=true;')
        dot += line('size="7,7";')
        for cl in self.classes:
            dot += cl.definitions()
        for fn in self.funcalls:
            dot += line('%s;' % fn.name)
        for imp in self.imports:
            dot += imp.definitions(subgraph=True)
        if subgraph:
            dot += line('}')
        return dot

    def relationships(self):
        dot = ''
        dot += line('/* relationships */')
        for fn in self.funcalls:
            for fc in fn.calls:
                dot += line('%s -> %s;' % (fn.name, fc.name))
        for cl in self.classes:
            dot += cl.relationships()
        for imp in self.imports:
            dot += imp.relationships()
        return dot

    def open(self):
        return line('digraph %s {' % self.name)

    def close(self):
        return line('}')

    def todot(self):
        dot = ''
        dot += self.open()
        dot += self.definitions()
        dot += self.relationships()
        dot += self.close()
        return dot

    def __str__(self):
        return self.todot()

def make_name(x, y, sep='_'):
    return x + sep + y

def line(x):
    return x + '\n'

def isiterable(x):
    return isinstance(x, (tuple, list, set))

def recapply(ast, cls, data):
    """Iteratively apply a class constructor to the parser list."""
    try:
        tmp = cls().parse(ast)
        del ast[0]
        if isiterable(tmp):
            data.update(tmp)
        else:
            data.add(tmp)

    except:
        pass

    finally:
        for item in ast[1:]:
            if isiterable(item):
                recapply(item, cls, data)

if __name__ == '__main__':
    global COMPLETE_NAME
    global EXCLUDE_CLASSES

    oparser = OptionParser()
    oparser.add_option('-f', '--file',            dest='infile',          default=sys.stdin,  type='string',
                       help='Input file [stdin by default]')
    oparser.add_option('-o', '--output',          dest='outfile',         default=sys.stdout, type='string',
                       help='Output file [stdout by default]')
    oparser.add_option('-i', '--incomplete_name', dest='incomplete_name', default=False,      action='store_true',
                       help='Do not prepend module names to imported functions')
    oparser.add_option('-x', '--exclude_classes', dest='exclude_classes', default=False,      action='store_true',
                       help='Do not create a subgaph for classes')
    oparser.add_option('-r', '--recursion_level', dest='reclevel',        default=0,          type='int',
                       help='Maximum level of recursion in scanning imported modules')

    (options, args) = oparser.parse_args()

    infile = options.infile
    if isinstance(infile, str):
        infile = open(infile, 'r')

    outfile = options.outfile
    if isinstance(outfile, str):
        outfile = open(outfile, 'w')

    COMPLETE_NAME = not options.incomplete_name
    EXCLUDE_CLASSES = options.exclude_classes
    reclevel = options.reclevel

    data = FileInput(infile, maxreclevel=reclevel)

    outfile.write(str(data))
