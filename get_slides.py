#!/usr/bin/env python
# TODO: add exception handling and more
# TODO: adding some threading with threading or multitas

import re, urllib2, os
import logging
from sys import exit

BAD_ARGS = 1
DEF_EXTS = ('pdf', 'txt')

logging.basicConfig(level=logging.INFO)

from optparse import OptionParser, make_option

def parse_page(base, ext):
    "Parse a webpage returning all urls of given extension "
    res = urllib2.urlopen(base).read()
    reg_ext = "|".join(ext)
    # ?: is necessary to avoid matching also of extension
    exp = "HREF=\"(\S+?.(?:" + reg_ext + "))\""
    links = re.compile(exp, re.IGNORECASE)
    return links.findall(res)

def download_stuff(down_urls, base, dest = os.getcwd(),
                   relative = True, enum = True):
    " Download all the urls given "
    base = re.match("(.+/).*", base).groups()[0]
    logging.debug("downloading from %s" % base)

    for (i, u) in enumerate(down_urls):
        # checking if it's an absolute or relative address
        if not("http" in u):
            doc = os.path.join(base, u)

        # absolute url, don't download it if relative set
        elif relative:
            continue

        name = u.split("/")[-1]
        if enum:
            name = "_".join([str(i), name])

        logging.info("fetching %s" % doc)
        # finally write to file
        open(os.path.join(dest, name), 'w').write(urllib2.urlopen(doc).read())

if __name__ == '__main__':
    # check how verbosity works!
    opt_list = [
        make_option("-v", "--verbose", action = "store_true", dest = "verbose"),
        make_option("-d", "--dest", dest = "dest", default = "slides"),
        make_option("-e", "--ext", dest = "extensions",
                     default = DEF_EXTS,
                     help = "list of extensions of files to download"),
        make_option("-n", "--enumerate", dest="enum", action = "store_true",
                     help = "if True number the documents in the found order"),
        make_option("-r", "--relative", dest="relative", action = "store_false",
                     help = "downloads only relative files, not absolute urls")]

    opt_parser = OptionParser(usage="get_slides.py [options] base_url1 ...",
                              option_list = opt_list)
    (options, args) = opt_parser.parse_args()
    print options, args

    if not args:
        print opt_parser.get_usage()

    if options.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # creating destination directory if not existing
    if not(os.path.exists(options.dest)):
        logging.info("creating directory")
        os.makedirs(options.dest)

    for base_url in args:
        logging.info("starting to download from %s" % base_url)

        urls = parse_page(base_url, options.extensions)
        download_stuff(urls, base_url, dest = options.dest,
                       relative = options.relative, enum = options.enum)
