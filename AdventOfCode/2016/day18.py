import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq

def get_first_line(test=False):
    path = 'inputs/day18.txt'
    if test:
        path = 'inputs/day18.txt'
    with open(path) as f:
        line = f.readline().strip()
    return line

def get_next_line(prev_line):
    p2 = prev_line[:]
    line_length = len(prev_line)
    p2 = p2 + '.'
    new_line = ''
    for i, square in enumerate(prev_line):
        if p2[i-1] != p2[i+1]:
            new_line = new_line + '^'
        else:
            new_line = new_line + '.'
    return new_line


def count_safe_tiles(lines):
    safe = 0
    for line in lines:
        for c in line:
            if c == '.':
                safe += 1
    return safe


    

def part1():
    lines = ['..^^.']
    lines = ['.^^.^.^^^^']
    lines = [get_first_line(True)]
    while len(lines) < 40:
        lines.append(get_next_line(lines[-1]))

    
    n_safe_tiles = count_safe_tiles(lines)

    print('Part 1: Number of safe tiles is {}'.format(n_safe_tiles))

def part2():
    lines = [get_first_line(True)]
    while len(lines) < 400000:
        lines.append(get_next_line(lines[-1]))

    
    n_safe_tiles = count_safe_tiles(lines)

    
    print('Part 2: Number of safe tiles for 400000 rows is {}'.format(n_safe_tiles))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
