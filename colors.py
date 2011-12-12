#!/usr/bin/env python2

COLORS = map(str, range(31,38))
RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = COLORS

CONTROL_SEQ = "\033[0;%sm"

def colorize_string(col, s):
    pre = CONTROL_SEQ % col
    after = CONTROL_SEQ % "0"
    return pre + s + after


def next_color(color):
    return COLORS[(COLORS.index(color) + 1) % len(COLORS)]


m = "message"
for c in COLORS:
    print(colorize_string(c, m))
