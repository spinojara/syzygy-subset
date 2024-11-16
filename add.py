#!/usr/bin/env python3

import sys

file = open('7P-SYZYGY-LIST', 'r')
out = open('7P-SYZYGY-SUM', 'w')
first = True
val = 0
tb = ''
for line in file:
    if not first and tb != line.split('.')[0]:
        sys.exit(1)
    tb = line.split('.')[0]
    val += int(line.split(' ')[1])

    if not first:
        out.write(f'{tb} {val}\n')
        val = 0

    first = not first
