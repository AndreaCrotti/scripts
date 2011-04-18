#!/usr/bin/env python

import subprocess

FMT = [("first name", "fn"),
       ("last name", "ln"),
       ("home mail", "he"),
       ("work mail", "we"),
       ("other mail", "oe"),
       ("birthday", "b")]

cmd = "contacts -H -S -f '%s'" % (';'.join('%' + x[1] for x in FMT))

proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out, err = proc.communicate()

org_contact_template = """* %s
:PROPERTIES:
:EMAIL:   %s
:END:
"""

for line in out.splitlines():
    s = line.split(';')
    for x in range(2, 5):
        if s[x]:
            mail_pref = FMT[x][0].split(' ')[0]
            name = ' '.join((s[0], s[1], mail_pref))
            print org_contact_template % (name, s[x])
