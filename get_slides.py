#!/usr/bin/env python

# TODO: add exception handling and more
# TODO: adding some threading with threading or multitas

import re, urllib2, os
import logging

BAD_ARGS = 1

logging.basicConfig(level=logging.INFO)

from optparse import OptionParser, make_option

def parse_page(base, regexp):
    "Parse a webpage returning all urls of given extension "
    res = urllib2.urlopen(base).read()
    reg_ext = "|".join(regexp)
    exp = "HREF=\"(\S+(?:.*?" + reg_ext + "))\""
    logging.debug("exp = %s" % exp)
    links = re.compile(exp, re.IGNORECASE)
    return links.findall(res)

# FIXME: make it more nice
def download_stuff(down_urls, base, dest):
    " Download all the urls given "
    for url in down_urls:
        doc = base + url
        name = os.path.join(dest, url.split("/")[-1])
        logging.info("writing file to %s" % name)
        open(os.path.join(name), 'w').write(urllib2.urlopen(doc).read())

if __name__ == '__main__':
    # check how verbosity works!
    opt_list = [
        make_option("-v", "--verbose", action = "store_true", dest = "verbose"),
        make_option("-d", "--dest", dest = "dest"),
        make_option("-p", "--pretend", dest = "pretend", action = "store_true", default = False),
        make_option("-r", "--regexp", dest = "regexp", help = "regexp of files to download")]

    opt_parser = OptionParser(usage="get_slides.py [options] base_url1 ...",
                              option_list = opt_list)

    (options, args) = opt_parser.parse_args()
    logging.debug(str(options))

    if not args:
        print opt_parser.get_usage()

    if options.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # creating destination directory if not existing
    if options.dest and not(os.path.exists(options.dest)):
        dest = options.dest
        logging.info("creating directory")
        os.makedirs(options.dest)

    else:
        dest = os.getcwd()

    for base_url in args:
        logging.info("starting to analyze %s" % base_url)

        urls = parse_page(base_url, tuple(options.regexp.split(",")))
        
        if not(options.pretend):
            download_stuff(urls, base_url, dest = dest)
        
        else:
            for u in urls:
                print u
