from datetime import datetime as dt
import sys
import numpy as np
import re
from collections import defaultdict, Counter

patterns = {}
full_pattern = {}

def get_data(is_test):
    if is_test:
        in_file = 'inputs/day16.test.txt'
    else:
        in_file = 'inputs/day16.txt'
    
    with open(in_file) as f:
        signal = f.read().strip()

    return signal
 
def part2(data):
    return None

def run_phase(signal):
    pattern = get_full_pattern(len(signal))
    return  np.abs(np.dot(pattern, signal))%10

def get_full_pattern(length):
    if length not in full_pattern:
        lines = []
        for i in range(1, length+1):
            lines.append(get_pattern(i, length))
        full_pattern[length] = np.array(lines)
    return full_pattern[length]

def get_pattern(n, length):
    if (n, length) not in patterns:
        pattern = [0,1,0,-1]
        pattern = np.array([n * [x] for x in pattern])
        pattern_2 = pattern[:]
        while np.prod(pattern.shape) < length + 1:
            pattern = np.concatenate([pattern_2, pattern])
        patterns[(n, length)] = pattern.flatten()[1:length+1]
    return patterns[(n, length)]

def part1(data):
    signal = [int(x) for x in data]
    for i in range(100):
        signal = run_phase(signal)
    return ''.join([str(x) for x in signal])[0:8]


def part2(signal, phases=100):
    # it looks like we can "cheat" a bit. The offset is not small, 
    # indeed the offset appears to always be larger than 
    # 1/2 of the extended array. If ou look at the pattern for such, 
    # for each element in the last half of the array,
    # the resultant element after running a phase is such that 
    # x'[i] = sum(x[i:]). 
    
    offset = int(signal[0:7])
    
    offset_mod = offset % (len(signal))
    
    # get the signal and 'rotate' it such that it begins at the offset (modulo natch)
    signal = [int(x) for x in signal]
    signal = signal[offset_mod:] + signal[:offset_mod]
    
    expected_length = 10000 * len(signal) - offset
    
    signal = (signal * (1 + int(expected_length / len(signal))))
    signal = signal[0:expected_length]
    
    # undergoign a phase, each element s[i] -> sum(s[i:])
    # we cam take advantage of numpy awesomeness by reversing
    # the array and using cumsum
    signal = np.flip(signal)
    for _ in range(phases):
        signal = np.cumsum(signal)%10
    signal = np.flip(signal)
    return ''.join(map(str, signal[:8]))

def main():
    
    is_test = False
    #is_test = True
    data = get_data(is_test)
    part_a = part1(data)
    print('Part 1: {}'.format(part_a))
    part_b = part2(data)
    print('Part 2: {}'.format(part_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
