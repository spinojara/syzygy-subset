#!/usr/bin/env python3

import sys

piecescore = { 'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0 }

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} GiB')
    sys.exit(1)

total = 1024 ** 3 * int(sys.argv[1])

def filter_tb(tb):
    return 'NNN' in tb or 'BBB' in tb or 'RRR' in tb or 'QQQ' in tb or tb == 'KQPPPvKQ' or tb == 'KRPPPvKR' or ('PPP' in tb and tb.endswith('vKN'))

def score(pieces):
    s = 0
    for c in pieces:
        s += piecescore[c]
    return s

def score_diff(tb):
    tb = tb.split('v')
    white = score(tb[0])
    black = score(tb[1])
    return abs(white - black)

file = open('7P-SYZYGY-DATA', 'r')

tbs = []
for line in file:
    line = line.strip().split(' ')
    tbs.append((line[0], int(line[1]), float(line[2]), float(line[3])))

tbs.sort(key=lambda x: -x[2] / x[1])

accumulated = 0
for tb in tbs:
    std = tb[3]
    s = tb[2]
    byte = tb[1]
    tb = tb[0]

    sd = score_diff(tb)
    if std < 0.10 or sd > 3 or (sd > 2 and ('Q' in tb or 'R' in tb)) or filter_tb(tb):
        continue
    if accumulated + byte > total:
        print(f'skipping: {tb} {byte / 1024 ** 3:.1f} GiB         {s} {std} {sd}')
        continue
    accumulated += byte
    print(f'{tb} {byte / 1024 ** 3:.1f} GiB         {s} {std} {sd}')

print(f'{accumulated / 1024 ** 3:.1f} GiB')
