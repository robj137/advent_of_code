import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day12.test.txt'
    else:
        in_file = 'inputs/day12.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    steps = []
    for line in lines:
        instruction = line[0]
        value = int(line[1:])
        steps.append((instruction, value))
    return steps

def get_directionals_dict():
    directionals = {}
    directionals['N'] = 1j
    directionals['E'] = 1
    directionals['S'] = -1j
    directionals['W'] = -1
    return directionals

def part1(data):
    directionals = get_directionals_dict()
    pos = 0 + 0j
    momentum = 1

    for i, val in data:
        if i in directionals:
            pos += directionals[i] * val
        elif i in ['R','L']:
            # momentum change
            rot = 1 if i == 'R' else -1
            while val:
                momentum *= ((-1j) * rot)
                val -= 90
        elif i == 'F':
            pos += momentum * val
    return int(abs(pos.imag) +abs(pos.real))

def part2(data):
    waypoint = 10 + 1j
    pos = 0 + 0j

    directionals = get_directionals_dict()

    for i, val in data:
        if i in directionals.keys():
            waypoint += directionals[i] * val
        elif i in ['L', 'R']:
            rot = 1 if i == 'R' else -1
            while val:
                waypoint *= ((-1j) * rot)
                val -= 90
        elif i == 'F':
            pos += waypoint * val
    return int(abs(pos.imag) + abs(pos.real))


if __name__ == '__main__':
    begin = dt.now()
    data = get_data(False)

    p1 = part1(data)
    print('Part 1: {}'.format(p1))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    p2 = part2(data)
    print('Part 2: {}'.format(p2))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
