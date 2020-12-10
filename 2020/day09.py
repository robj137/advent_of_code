import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day09.test.txt'
    else:
        in_file = 'inputs/day09.txt'
    
    with open(in_file) as f:
        lines = [int(x.strip()) for x in f.readlines()]
 
    return lines


def get_paired_sums(l):
    # double loop over a list to get all possible sums of two elements
    N = len(l)
    sums = []
    for i in range(N):
        for j in range(i, N):
            sums.append(l[i] + l[j])
    return list(set(sums))

def part1(is_test=True):
    if is_test:
        n_pre = 5
    else:
        n_pre = 25
    data = get_data(is_test)
    candidates = []
    for i in range(len(data)):
        allowed = []
        if i >= n_pre:
            allowed.extend(get_paired_sums(data[i-n_pre:i]))
        candidates.append(allowed)

    bad_one = None
    pairs = zip(data[n_pre:], candidates[n_pre:])
    for a, b in pairs:
        if a not in b:
            bad_one = a

    print("Odd one out is {}".format(bad_one))

    for i in range(len(data)):
        this_sum = data[i]
        for j in range(i+1, len(data)):
           this_sum += data[j]
           if this_sum == bad_one:
                small = min(data[i:j+1])
                large = max(data[i:j+1])
                print("Encryption Weakness: {}".format(small+large))


if __name__ == '__main__':
    begin = dt.now()
    #main()
    part1(is_test=False)
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #part2()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
