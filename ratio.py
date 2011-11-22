#!/usr/bin/env python2

import argparse

from PIL import Image
DEFAULT_THRESHOLD = 0.01
DEFAULT_RATIO = 0.75

def pic_ratio(imgpath):
    img = Image.open(imgpath)
    w, h = img.size
    return float(w) / h


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='show the ratio')
    parser.add_argument('-r', '--desired-ratio',
                        default=DEFAULT_RATIO)

    parser.add_argument('pic',
                        nargs='+')

    ns = parser.parse_args()
    for p in ns.pic:
        cr = pic_ratio(p)
        if abs(cr - DEFAULT_RATIO) > DEFAULT_THRESHOLD:
            print("picture %s has to be fixed, has ratio %s" % (p, str(cr)))
