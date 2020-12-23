import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day15.test.txt'
    else:
        in_file = 'inputs/day15.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    return [int(x) for x in lines[0].split(',')]


def run(data, N=2020):
    time = 0
    numbers = {}
    prev_num = None
    pre_data = data[:-1]
    for num in pre_data:
        time += 1
        numbers[num] = time
    prev_said = data[-1]

    for i in range(len(numbers), N-1):
        time += 1
        if prev_said not in numbers:
            numbers[prev_said] = time
            to_say = 0
        else:
            to_say = time - numbers[prev_said]
            numbers[prev_said] = time
        prev_said = to_say

    return prev_said

if __name__ == '__main__':
    begin = dt.now()
    data = get_data(False)
    p1 = run(data, 2020)
    print('Part 1: {}'.format(p1))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    p2 = run(data, 30000000)
    print('Part 2: {}'.format(p2))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
