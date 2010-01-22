#!/usr/bin/python
# encoding: utf-8
# TODO: using a logger and creating some tests to check correctness

import sys
import socket
import os
import pickle
import urllib2
    
from re import search
from getopt import getopt

VERBOSE = False

CONF = dict([
    ('conf_file', os.getenv('HOME') + '/.authconf'),
    ('proxy_addr', 'proxy.science.unitn.it'),
    ('proxy_port', 3128),
    ('authgate_addr', '193.205.213.40'),
    ('authgate_port', 54273),
    ('u_name', 'blabla'),
    ('u_sname', 'blabla'),
    ('u_mail', 'mymail@studenti.unitn.it'),
    ('mode', 1)
    ])

BAD_USAGE   = 1
PROXY_ERROR = 3
NOT_CONNECTED   = 4


def get_data():
    """gets the data to break the proxy"""
    if VERBOSE:
        print "[+] authentication data:\n   name:\t%s\n   sname:\t%s\n   mail:\t%s\n   mode:\t%i" % \
            (CONF['u_name'], CONF['u_sname'], CONF['u_mail'], CONF['mode'])
    page = get_google()
    # very simple pattern matching
    https_string = search(r'https.*?"', page)
    if not https_string:
        print "[!!] proxy error"
        sys.exit(PROXY_ERROR)

    url = page[https_string.start() : https_string.end()]
    # most important thing is the random token
    data = urllib2.urlparse.urlsplit(url)[3].split('&')
    data_dict = dict([x.split('=') for x in data])
    return data_dict

def send_data(host, port, request):
    """Send data over a socket and return te output"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request)
    response = s.recv(1024)
    s.close()
    return response

def connection(data):
    if VERBOSE:
        print "[+] connecting to the network"
    request = "GET " + " HTTP/1.1\r\nHost: " + data['raddr'] + "\r\nKeep-Alive: 300\r\n\r\n\""
    send_data(CONF['proxy_addr'], CONF['proxy_port'], request)

def bypass(data):
    """Bypass the proxy authentication"""
    if VERBOSE:
        print "[+] bypassing the proxy authentication"
    auth_request = "authenticate\t%s\t%s %s\t%s\t%s\t%i\n" % \
        (data['raddr'], CONF['u_name'], CONF['u_sname'], CONF['u_mail'], data['token'], CONF['mode'])
    send_data(CONF['authgate_addr'], CONF['authgate_port'], auth_request)

def disconnect(data):
    """Logout from the session"""
    print "[+] disconnecting from auth network"
    request = "revoke\t%s\t%s\r\n" % (data['raddr'], data['token'])
    send_data(CONF['authgate_addr'], CONF['authgate_port'], request)

def get_google():
    if VERBOSE:
        print "[+] downloading google page to get the parameters"
    try:
        page = urllib2.urlopen("http://www.google.it").read()
    except urllib2.URLError:
        print "[!!] not connected to the network"
        sys.exit(NOT_CONNECTED)
    else:
        return page

def is_authenticated():
    """boolean check to see if already authenticated"""
    return 'google' in get_google()
    
def usage():
    print """auth_bypass.py [-d] [-v]
    By default it log into the proxy with some default values. """
    sys.exit(BAD_USAGE)

def main():
    opts, _ = getopt(sys.argv[1:], "vd")
    os.environ['http_proxy'] = ":".join([CONF['proxy_addr'], str(CONF['proxy_port'])])
    for o, a in opts:
        if o == '-v':
            global VERBOSE
            VERBOSE = True
        if o == '-d':
            if not is_authenticated():
                print "[+] you're already disconnected, no need"
            else:
                if not os.path.exists(CONF['conf_file']):
                    print "[!!] you didn't connect with this script, can't disconnect automatically"
                else:
                    data = pickle.load(open(CONF['conf_file']))
                    disconnect(data)
                    if not is_authenticated():
                        print "[+] disconnected, removing configuration file"
                       # eliminate conf file
                        os.remove(CONF['conf_file'])
                    else:
                        print "[!!] not able to disconnect"
                    sys.exit(0)
                        
    if is_authenticated():
        print "[+] already authenticated"
        sys.exit(NOT_CONNECTED)
    else:
        # setting globally the proxy
        data = get_data()
        connection(data)
        bypass(data)
        if is_authenticated():
            print "[+] succesfully authenticated, saving data to ", CONF['conf_file']
            pickle.dump(data, open(CONF['conf_file'], 'w'))
        else:
            print "[!!] not able to authenticate to the proxy"            
 
if __name__ == '__main__':
    main()
