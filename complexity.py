#!/usr/bin/env python3

import json
import math

tbs = json.load(open('stats.json', 'r'))

infile = open('7P-SYZYGY-FREQ', 'r')
outfile = open('7P-SYZYGY-DATA', 'w')

for line in infile:
    line = line.strip().split(' ')
    tb = line[0]
    byte = line[1]
    freq = line[2]

    wins = tbs[tb]['histogram']['white']['wdl']['2'] + tbs[tb]['histogram']['white']['wdl']['1'] + tbs[tb]['histogram']['black']['wdl']['-2'] + tbs[tb]['histogram']['black']['wdl']['-1']
    losses = tbs[tb]['histogram']['white']['wdl']['-2'] + tbs[tb]['histogram']['white']['wdl']['-1'] + tbs[tb]['histogram']['black']['wdl']['2'] + tbs[tb]['histogram']['black']['wdl']['1']
    draws = tbs[tb]['histogram']['white']['wdl']['0'] + tbs[tb]['histogram']['black']['wdl']['0']
    total = wins + losses + draws
    mean = (wins - losses) / total
    var = (wins * (1 - mean) ** 2 + draws * (0 - mean) ** 2 + losses * (-1 - mean) ** 2) / (total - 1)
    std = math.sqrt(var)

    print(f'{tb} {losses / total:.3f} {draws / total:.3f} {wins / total:.3f} {std}')
    
    outfile.write(f'{tb} {byte} {freq} {std:.3}\n')
