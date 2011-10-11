#!/usr/bin/env python2
import csv
from itertools import izip
from sys import argv

# TODO: make it configurable
# - number of header lines to skip
# - tolerance
# - output format
# - files to give in input

ST = "Value %f in file 1 (line %d) differs by %d from %f in file 2"
SKIP_LINES = 3

tolerance = 0.02

def compute_diff(val1, val2):
    if val2 == 0:
        print("second value == 0")
        return 0
    return abs(val1 / val2) / val1

r1 = csv.reader(open(argv[1]))
r2 = csv.reader(open(argv[2]))
# skip first line
for i in range(SKIP_LINES):
    r1.next(); r2.next()

for val1, val2 in izip(r1, r2):
    for i in range(len(val1)):
        v1, v2 = float(val1[i]), float(val2[i])
        diff = compute_diff(v1, v2)
        if diff > tolerance:
            print(ST % (v1, i, diff * 100, v2))
