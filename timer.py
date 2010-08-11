#!/usr/bin/env python
"""
Creates a nice timer, using nice colors and splitting the screen accordingly
"""

import time
import sys
import os

COLORS = map(str, range(31,38))
RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = COLORS

control = lambda col: "\033[0;" + col + "m"
colorize = lambda col, s: control(col) + s + control("0")


def next_color(color):
    return COLORS[(COLORS.index(color) + 1) % len(COLORS)]

# works on linux and osx
rows, columns = map(int, os.popen('stty size', 'r').read().split())

os.system("clear")
 
if len(sys.argv) < 2:
    print "usage: %s <time1> <time2> <time3> ..."

intervals = map(int, sys.argv[1:])
tot = sum(intervals)
# computing the subtototals
subtots = [sum(intervals[:i+1]) for i in range(len(intervals))]

# delay of the function
delay = float(tot) / rows

def print_string(color):
    print colorize(color, "*" * columns)

col = GREEN
tot_time = 0
pos = 0

while True:
    if pos == len(subtots):
        break

    print_string(col)
    time.sleep(delay)
    tot_time += delay

    if tot_time >= subtots[pos]:
        col = next_color(col)
        pos += 1
    
