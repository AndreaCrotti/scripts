#!/usr/bin/env python2

from glob import glob
from PIL import Image


def make_contact_sheet(fnames,(ncols,nrows),(photow,photoh),
                       (marl,mart,marr,marb), padding):

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize((photow,photoh)) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew


def compose(ext):
    files = glob("*.%s" % ext)
    # Don't bother reading in files we aren't going to use
    ncols, nrows = 4, 3
    if len(files) > ncols*nrows: 
        files = files[:ncols*nrows]

    # These are all in terms of pixels:
    photow, photoh = 200,150
    photo = (photow, photoh)

    margins = [5,5,5,5]

    padding = 1

    inew = make_contact_sheet(files, (ncols, nrows), photo, margins, padding)
    output = "bs.png"
    print("saving to %s" % output)
    inew.save(output)

compose('jpg')
