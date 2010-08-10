#!/usr/bin/python
# Copyright 2008 Marcus D. Hanwell <marcus@cryos.org>
# Distributed under the terms of the GNU General Public License v2 or later
# For example we have something like
# commit ae6de05351cbc00205b4461757d01be2d7408758
# Author: Andrea Crotti <andrea.crotti.0@gmail.com>
# Date:   2010-08-04

#  bar.sh        |   41 +++++++++++++++++++++++++++++++++++++++++
#  c_gprof.sh    |    7 ++-----
#  org_export.sh |   43 ++++++++++++++++++++++++-------------------
#  scapier.py    |   11 +++++++++++
#  testmerge.sh  |    2 +-
#  timer.py      |    8 ++++++++
#  6 files changed, 87 insertions(+), 25 deletions(-)
#  create mode 100755 bar.sh
#  create mode 100644 scapier.py
#  create mode 100644 timer.py

# commit 8c7f0a00d1cbd4e3b2d4ac95a9c7039084de9b59
# Author: Andrea Crotti <andrea.crotti.0@gmail.com>
# Date:   2010-07-13

#     adding more scripts

#  create_turbo.sh    |    7 +++++++
#  git_interactive.sh |   12 ++++++++++++
#  testmerge.sh       |   14 ++++++++++++++
#  3 files changed, 33 insertions(+), 0 deletions(-)
#  create mode 100755 create_turbo.sh
#  create mode 100755 git_interactive.sh
#  create mode 100755 testmerge.sh

import string
import re
import sys
import os
import subprocess

def gitlog_to_changelog(output):
    # Execute git log with the desired command line options.
    fin = os.popen('git log --summary --stat --no-merges --date=short', 'r')
    # Create a ChangeLog file in the current directory.
    fout = open('ChangeLog.try', 'w')

    # Set up the loop variables in order to locate the blocks we want
    authorFound = False
    dateFound = False
    messageFound = False
    filesFound = False
    message = ""
    messageNL = False
    files = ""
    prevAuthorLine = ""

    "converts the git log to a changelog"
    for line in fin:
        # The commit line marks the start of a new commit object.
        if string.find(line, 'commit') >= 0:
            # Start all over again...
            authorFound = False
            dateFound = False
            messageFound = False
            messageNL = False
            message = ""
            filesFound = False
            files = ""
            continue
        # Match the author line and extract the part we want
        elif re.match('Author:', line) >=0:
            authorList = re.split(': ', line, 1)
            author = authorList[1]
            author = author[0:len(author)-1]
            authorFound = True
        # Match the date line
        elif re.match('Date:', line) >= 0:
            dateList = re.split(':   ', line, 1)
            date = dateList[1]
            date = date[0:len(date)-1]
            dateFound = True
        # The svn-id lines are ignored
        elif re.match('    git-svn-id:', line) >= 0:
            continue
        # The sign off line is ignored too
        elif re.search('Signed-off-by', line) >= 0:
            continue
        # Extract the actual commit message for this commit
        elif authorFound & dateFound & messageFound == False:
            # Find the commit message if we can
            if len(line) == 1:
                if messageNL:
                    messageFound = True
                else:
                    messageNL = True
            elif len(line) == 4:
                messageFound = True
            else:
                if len(message) == 0:
                    message = message + line.strip()
                else:
                    message = message + " " + line.strip()
        # If this line is hit all of the files have been stored for this commit
        elif re.search('files changed', line) >= 0:
            filesFound = True
            continue
        # Collect the files for this commit. FIXME: Still need to add +/- to files
        elif authorFound & dateFound & messageFound:
            fileList = re.split(' \| ', line, 2)
            if len(fileList) > 1:
                if len(files) > 0:
                    files = files + ", " + fileList[0].strip()
                else:
                    files = fileList[0].strip()
        # All of the parts of the commit have been found - write out the entry
        if authorFound & dateFound & messageFound & filesFound:
            # First the author line, only outputted if it is the first for that
            # author on this day
            authorLine = date + "  " + author
            if len(prevAuthorLine) == 0:
                fout.write(authorLine + "\n")
            elif authorLine == prevAuthorLine:
                pass
            else:
                fout.write("\n" + authorLine + "\n")

            # Assemble the actual commit message line(s) and limit the line length
            # to 80 characters.
            commitLine = "* " + files + ": " + message
            i = 0
            commit = ""
            while i < len(commitLine):
                if len(commitLine) < i + 78:
                    commit = commit + "\n  " + commitLine[i:len(commitLine)]
                    break
                index = commitLine.rfind(' ', i, i+78)
                if index > i:
                    commit = commit + "\n  " + commitLine[i:index]
                    i = index+1
                else:
                    commit = commit + "\n  " + commitLine[i:78]
                    i = i+79

            # Write out the commit line
            fout.write(commit + "\n")

            #Now reset all the variables ready for a new commit block.
            authorFound = False
            dateFound = False
            messageFound = False
            messageNL = False
            message = ""
            filesFound = False
            files = ""
            prevAuthorLine = authorLine

        # Close the input and output lines now that we are finished.
        fin.close()
        fout.close()

class ChangeLogEntry(object):
    def __init__(self, **kwargs):
        "stores an entry"
        self.entry = kwargs
        self.format = """
%(date)s %(author)s
* %(files)s: %(msg)s
"""

    def __str__(self):
        try:
            return self.format % self.entry
        except KeyError:
            # is that correct to trap an exception and return a string with the error?
            return "not enough arguments passed"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "./%s <destination_file>" % sys.argv[0]
        
    c = ChangeLogEntry(author="Andrea", msg="first commit", date="12 2 2200", files="uno due tre")
    print c
