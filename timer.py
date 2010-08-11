#!/usr/bin/env python
"""
Creates a nice timer, using nice colors and splitting the screen accordingly
"""

import time
import sys
import os
import getopt

# works on linux and osx
# TODO: add a warning for it 
rows, columns = map(int, os.popen('stty size', 'r').read().split())

# TODO: use colors also if possible
os.system("clear")
 
intervals = map(int, sys.argv[1:])
# print "intervals = %s" % str(intervals)
tot = sum(intervals)

# delay of the function
delay = float(tot) / rows

for x in range(rows):
    print " *** "
    time.sleep(delay)

# def makerepeater(delay, fun, *a, **k):
#     def wrapper(*a, **k):
#         while True:
#             fun(*a, **k)
#             time.sleep(delay)
#     return wrapp


#define CONTROL(color) "\033[0;"color"m"
#define RED "31"
#define GREEN "32"
#define YELLOW "33"
#define BLUE "34"
#define MAGENTA "35"
#define CYAN "36"
#define WHITE "37"
