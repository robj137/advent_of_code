import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day10.test.txt'
    else:
        in_file = 'inputs/day10.txt'
    
    with open(in_file) as f:
        lines = [int(x.strip()) for x in f.readlines()]
 
    return lines

def get_clean_data(is_test=True):
    data = get_data(is_test)
    built_in_joltage = max(data) + 3
    data.append(max(data) + 3)  # built-in joltage
    data.append(0)  # charging outlet joltage
    data.sort()
    data.reverse()
    return data

def part1(data):
    # we've already sorted and reversed the data, so just 
    # keep tabs on the joltage differences
    diffs = []
    adapters = data[:]
    joltage = adapters.pop()
    while adapters:
        new_joltage = adapters.pop()
        diff = new_joltage - joltage
        diffs.append(diff)
        joltage = new_joltage
    
    # cheat by using Counter library, and grab the '1' and '3' diffs
    c = Counter(diffs)
    n1 = c[1]
    n3 = c[3]
    
    print('Part 1: Number of 3-jolt diffs time 1-jolt diffs: {}'.format(n1 * n3))

def part2(data):
    # just start at one end and keep track of all the ways each adapter can connect
    # to the adapters that came before
    data = data[:]
    m = {}
    
    # start at one end, and there's only one way to do that :)
    el = data.pop(0)
    m[el] = 1
    while data:
        el = data.pop(0)
        multiplier = 0
        # this wouldn't really scale (i mean it would scale like N^2), but it's fine for this
        # could just keep a short list of the last three elements instead check thoe instead
        for key in m:
            if key - el <= 3:
                multiplier += m[key]
        m[el] = multiplier
    print('Part 2: Soo many ways: {}'.format(m[0]))

if __name__ == '__main__':
    begin = dt.now()
    #main()
    data = get_clean_data(is_test=False)
    part1(data)
    part_1_time = dt.now()
    diff_time = part_1_time - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part2(data)
    diff_time = dt.now() - part_1_time
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
