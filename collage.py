#!/usr/bin/env python2

import argparse
from glob import glob
from os import path

from PIL import Image

MARGINS = (5,5,5,5)
PADDING = 1
PIC_SIZE = (300, 400)
DEFAULT_FNAME = 'collage'
DEFAULT_EXT = 'png'


def make_contact_sheet(fnames, nrows, ncols, background):

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize(PIC_SIZE) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marl, marr, mart, marb = MARGINS
    marw = marl+marr
    marh = mart+ marb
    photow, photoh = PIC_SIZE

    padw = (ncols - 1) * PADDING
    padh = (nrows - 1) * PADDING
    isize = (ncols*photow + marw + padw,nrows*photoh + marh + padh)

    # Create the new image. The background doesn't have to be white
    inew = Image.new('RGB', isize, background)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol * (photow+PADDING)
            right = left + photow
            upper = mart + irow * (photoh+PADDING)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            #TODO: fix this ugly loop
            try:
                img = imgs.pop(0)
            except:
                break
            # this is the important piece
            inew.paste(img,bbox)
    return inew


def compose(files, output, background):
    nrows, ncols = gen_rows_cols(len(files))
    if background == 'black':
        background = (0, 0, 0)
    else:
        background = (255, 255, 255)

    inew = make_contact_sheet(files, nrows, ncols, background)
    inew.save(output)


#TODO: add the possibility to create different shapes
def gen_rows_cols(tot):
    from math import sqrt, ceil
    rows = int(sqrt(tot))
    cols = int(ceil(float(tot) / rows))
    return rows, cols


def test_rows_cols():
    assert gen_rows_cols(12) == (3, 4)


def parse_arguments():
    parser = argparse.ArgumentParser(description='create a pictures collage')
    parser.add_argument('path',
                        help='path where pictures are stored')

    parser.add_argument('ext',
                        help='extension of the pictures')

    parser.add_argument('-m', '--mode',
                        choices=('fixed', 'moved'),
                        help='output modality')

    parser.add_argument('-w', '--width',
                        help='max resolution width')
    
    parser.add_argument('-o', '--output',
                        default='%s.%s' % (DEFAULT_FNAME, DEFAULT_EXT))

    parser.add_argument('-b', '--background',
                        choices=('white', 'black'),
                        default='white')

    parser.add_argument('-g', '--generate',
                        help='generate many random files')


    return parser.parse_args()

if __name__ == '__main__':
    ns = parse_arguments()
    to_glob = path.join(ns.path, "*.%s" % ns.ext)
    files = glob(to_glob)
    
    if ns.generate:
        from random import shuffle
        for n in range(int(ns.generate)):
            shuffle(files)
            compose(files, "%s_%d.%s" % (DEFAULT_FNAME, n, DEFAULT_EXT), ns.background)
    else:
        compose(files, ns.output, ns.background)
