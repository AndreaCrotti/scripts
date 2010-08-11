#!/usr/bin/env python

COLORS = map(str, range(31,38))
RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = COLORS

control = lambda col: "\033[0;" + col + "m"
colorize = lambda col, s: control(col) + s + control("0")


def next_color(color):
    return COLORS[(COLORS.index(color) + 1) % len(COLORS)]
