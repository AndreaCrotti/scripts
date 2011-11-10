#!/usr/bin/env python2

import sys

class ImportInspector(object):

    def find_module(self, module, path):
        print("importing module %s" % module)


if __name__ == '__main__':
    progname = sys.argv[0]
    # shift by one position
    sys.argv = sys.argv[1:]
    sys.meta_path.append(ImportInspector())

    code = compile(open(progname, 'rb').read(), progname, 'exec')
    exec(code)
