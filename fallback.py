#!/usr/bin/env python2
import sys

COUNTER = 0

def hello():
    global COUNTER
    print("hello %d" % COUNTER)
    COUNTER += 1


def main():
    while True:
        try:
            hello()
        except KeyboardInterrupt:
            print(locals())
            try:
                raw_input("any key to continue, C-c to quit")
            except KeyboardInterrupt:
                sys.exit(0)

if __name__ == '__main__':
    main()
