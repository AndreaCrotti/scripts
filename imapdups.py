#!/usr/bin/env python
# This tool generates on stdout a list of message IDs
# that occur twice on your imap server. It looks through
# all folders you have, so is really a resource hog!!
#
# You do need to edit the line to connect to your imap server.
# The example below works against your local dovecot server if
# you store your mail in /home/johannes/.mail (maildir!)
#
# To download from this site, append ?action=raw to the URL.
# If you want to use wget, do
#  $ wget -U wiki-download -O imap-find-duplicates http://johannes.sipsolutions.net/Projects/imap-find-duplicates?action=raw
#
# Copyright 2005 Johannes Berg <johannes@sipsolutions.net>
# Released under GPLv2
#

import imaplib

# edit this line:
conn = imaplib.IMAP4_stream('MAIL=/home/johannes/.mail /usr/lib/dovecot/imap')
# possibly add things here to log in to your server
# see http://docs.python.org/lib/module-imaplib.html

# no need to edit anything below here

def get_msg_id_list(connection, mailbox):
    status,dummy = connection.select(mailbox, True)
    if status != 'OK':
        return []
    
    status,list = conn.fetch('1:*', '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    if status != 'OK':
        return []
    if list == [None]:
        return []
    result = []
    for item in list:
        if type(item) == type(''):
            continue
        idhdr = item[1].strip()
        if idhdr == '':
            # if message has no msgid, we can't really use it
            continue
        result += [(idhdr, mailbox, int(item[0].split()[0]))]
    return result

status,list = conn.list()
boxes = []
for l in list:
    # FIXME: doesn't handle quotes in folder names!
    boxes += [l.split('"')[-2]]

mails = []
for box in boxes:
    mails += get_msg_id_list(conn, box)

conn.close()
mails.sort(lambda x,y: cmp(x[0],y[0]))

old = ('',)
printed=False
for m in mails:
    if old[0] == m[0]:
        if not printed:
            print old[0],': ',old[1],old[2],
            printed = True
        print ',',m[1],m[2],
    else:
        if printed:
            print ''
        printed=False
    old = m
