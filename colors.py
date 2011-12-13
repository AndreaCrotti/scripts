#!/usr/bin/env python2

import random
from string import ascii_letters

COLORS = map(str, range(31,38))
RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = COLORS

CONTROL_SEQ = "\033[0;%sm"

def colorize_string(col, s):
    pre = CONTROL_SEQ % col
    after = CONTROL_SEQ % "0"
    return pre + s + after


def next_color(color):
    return COLORS[(COLORS.index(color) + 1) % len(COLORS)]


def random_printer(dim):
    for i in range(dim):
        if random.random() > 0.1:
            l = random.choice(ascii_letters)
            print(colorize_string(random.choice(COLORS), l)),
        else:
            print(" "),

random_printer(100 * 100 * 10)
