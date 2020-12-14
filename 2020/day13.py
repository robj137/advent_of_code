import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day13.test.txt'
    else:
        in_file = 'inputs/day13.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]


    earliest = int(lines[0])
    shuttles = [int(x.replace('x', '-1')) for x in lines[1].split(',')]

    return earliest, shuttles




def part1(earliest, shuttles):
    shuttle_times = {}
    for shuttle in shuttles:
        if shuttle < 0:
            continue
        shuttle_times[shuttle] = []
        shuttle_time = 0
        while shuttle_time <=earliest + shuttle:
            if shuttle_time >= earliest:
                shuttle_times[shuttle].append(shuttle_time)
            shuttle_time += shuttle

    my_shuttle = None
    departure_time = 10 * earliest
    for shuttle_number in shuttle_times:
        this_time = shuttle_times[shuttle_number][0]
        if this_time < departure_time:
            departure_time = this_time
            my_shuttle = shuttle_number

    return my_shuttle * (departure_time - earliest)


def part2(shuttles):
    og_shuttles = shuttles[:]
    offset = 0
    multiplier = 1
    for i, shuttle in enumerate(shuttles):
        if shuttle < 0:
            continue
        
        candidates_a = [x for x in range(offset, multiplier * shuttle, multiplier)]
        for candidate in candidates_a:
            if (candidate + i) % shuttle == 0:
                match = candidate
        offset = match
        multiplier *= shuttle
    return offset



if __name__ == '__main__':
    begin = dt.now()
    earliest, shuttles = get_data(False)
    p1 = part1(earliest, shuttles)
    print('Part 1: {}'.format(p1))
    part1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    p2 = part2(shuttles)
    print('Part 2: {}'.format(p2))
    diff_time = dt.now() - part1_time
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
