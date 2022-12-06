import numpy as np
import sys
import re
from collections import defaultdict, Counter

def get_data(is_test=True):
    path = 'inputs/day08.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()

    displays = [x.strip().split(' | ') for x in lines]
    return displays

def parse_signal_patterns(p):
    if type(p) != list:
        p = p.split()
    
    segments = ''.join(p)
    segment_count = Counter(segments)
    top_left_segment = [x for x in filter(lambda x: segment_count[x] == 6, segment_count)][0]
    bottom_left_segment = [x for x in filter(lambda x: segment_count[x] == 4, segment_count)][0]
    d = {}

    for entry in p:
        e = ''.join(sorted(entry))
        if len(entry) == 2:
            d[1] = e
            d[e] = '1'
        elif len(entry) == 4:
            d[4] = e
            d[e] = '4'
        elif len(entry) == 3:
            d[7] = e
            d[e] = '7'
        elif len(entry) == 7:
            d[8] = e
            d[e] = '8'
    
    middle_segment = ''.join( set(d[4]).difference(set(d[1])).difference(top_left_segment))

    for entry in p:
        e = ''.join(sorted(entry))
        if len(e) == 5: # 2, 3, 5
            if set(e).issuperset(set(d[1])):
                d[3] = e
                d[e] = '3'
            elif set(e).issuperset(set(top_left_segment)):
                d[5] = e
                d[e] = '5'
            else:
                d[2] = e
                d[e] = '2'
        if len(e) == 6: # 0, 6, 9
            if middle_segment not in e:
                d[0] = e
                d[e] = '0'
            elif not set(e).issuperset(d[1]):
                d[6] = e
                d[e] = '6'
            else:
                d[9] = e
                d[e] = '9'

    return d


def part1(data):
    unique_count = 0
    for display in data:
        signal_pattern, output = display
        lengths = [len(x) for x in output.split()]
        unique_count += np.sum(np.array(lengths) == 2)
        unique_count += np.sum(np.array(lengths) == 4)
        unique_count += np.sum(np.array(lengths) == 7)
        unique_count += np.sum(np.array(lengths) == 3)

    print('Part 1: Unique count is {}'.format(unique_count))

def part2(data):
    s = 0
    for display in data:
        signal_pattern, output = display
        translation = parse_signal_patterns(signal_pattern)
        s += int(''.join([translation[''.join(sorted(x))] for x in output.split()]))
    print('Part 2: sum is {}'.format(s))

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
    part2(data)
