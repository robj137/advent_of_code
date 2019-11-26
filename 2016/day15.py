import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq


def get_discs(test=False):
    path = 'inputs/day15.txt'
    if test:
        path = 'inputs/day15.alt.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    p = 'Disc #([0-9]+) has ([0-9]+) positions; at time=([0-9]+), it is at position ([0-9]+).'
    discs = []
    for line in lines:
        result = re.search(p, line)
        if result:
            g = result.groups()
            num = int(g[0])
            size = int(g[1])
            time_offset = int(g[2])
            start_pos = int(g[3])
            d = deque(range(size))
            d.rotate(start_pos)
            d.rotate(time_offset)
            d.rotate(num)
            discs.append(d)
    return discs

def part1():
    discs = get_discs(False)
    i = 0
    while [d[0] for d in discs] != [0]*len(discs):
        [d.rotate() for d in discs]
        i += 1

    print('Part 1: It takes {} seconds to perfectly align the discs'.format(i))


def part2():
    discs = get_discs(False)
    new_disc = deque(range(11))
    new_disc.rotate(1 + len(discs))
    discs.append(new_disc)
    i = 0
    while [d[0] for d in discs] != [0]*len(discs):
        [d.rotate() for d in discs]
        i += 1

    print('Part 2: It takes {} seconds to perfectly align the (re-arranged) discs'.format(i))


def main():
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
