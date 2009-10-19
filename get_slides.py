#!/usr/bin/env python
# add some possible options to give
# Base link, destination directory, extenstion list, relative/non relative

import re, urllib2, os
import logging

logging.basicConfig(level=logging.INFO)

from optparse import OptionParser

def parse_page(base, ext = ('pdf', 'txt')):
    res = urllib2.urlopen(base).read()
    reg_ext = "|".join(ext)
    # ?: is necessary to avoid matching also of extension
    exp = "HREF=\"(\S+?.(?:" + reg_ext + "))\""
    links = re.compile(exp, re.IGNORECASE)
    return links.findall(res)

def download_stuff(urls, base, dest = os.getcwd(), relative = True, enum = True):
    base = re.match("(.+/).*", base).groups()[0]
    for (i, u) in enumerate(urls):
        # checking if it's an external link
        if not("http" in u):
            doc = os.path.join(base, u)

        # absolute url, don't download it
        elif relative:
            continue

        name = u.split("/")[-1]
        if enum:
            name = "_".join([str(i), name])

        print "fetching ", doc
        open(os.path.join(dest, name), 'w').write(urllib2.urlopen(doc).read())

if __name__ == '__main__':
    o = OptionParser()
    o.add_option("-b", "--base", dest = "base", 
                 help = "base link")
    # check how verbosity works!
    o.add_option("-v", "--verbose", help = "activate verbose mode",
                 default = "True")
    o.add_option("-d", "--dest", dest = "dest")
    o.add_option("-e", "--ext", dest = "extensions",
                 help = "list of extensions of files to download")
    (options, args) = o.parse_args()
    
    if not(os.path.exists(options.dest)):
        logging.info("creating directory")
        os.makedirs(options.dest)
    
    urls = parse_page(options.base)
    download_stuff(urls, options.base, dest = options.dest, relative = True, enum = True)
