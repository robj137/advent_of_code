import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq
import sys

def get_inputs(test=False):
    path = 'inputs/day20.txt'
    if test:
        path = 'inputs/day20.alt.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]

    return lines

def get_overlap(a, b):
    a, b = sorted([a,b]) # ensure a[0] < b[0]
    a1, a2 = a
    b1, b2 = b
    if a2 < b1:
        return None
    return (a1, b2)



def part1():
    lines = get_inputs()
    master_black_list = []
    for line in lines:
        a, b = [int(x) for x in line.split('-')]
        master_black_list.append((a,b))

    edges = []
    for a, b in master_black_list:
        edges.extend([a-1, a, a+1])
        edges.extend([b-1, b, b+1])

    edges.sort()
    edges = list(set(edges))
    edges.sort()
    lookup = {}
    for i, edge in enumerate(edges):
        lookup[edge] = i
    hist = [0] * (len(edges) + 1)
    for r in master_black_list:
        ra, rb = r
        na = lookup[ra]
        nb = lookup[rb]
        for i in range(na, nb+1):
            hist[i] += 1

    first = -1
    hist[0] = 1 # underflow edge doesn't coun
    for i in range(len(hist)-1):
        if hist[i] == 0:
            first = edges[i]
            break
    
    open_edges = []
    for i in range(len(hist)-1):
        if hist[i] == 0:
            open_edges.append((i,edges[i]))
    
    open_edges.pop()
    n_open = 0
    for ndx, val in open_edges:
        n_open += edges[ndx+1] - edges[ndx]


    return first, n_open

def main():
    
    first, n_open = part1()
    print('Part 1: First allowed IP is {}'.format(first))
    print('Part 2: Number of open IPs is {}'.format(n_open))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
