import pandas as pd
from collections import defaultdict
import numpy as np
import datetime as dt
from datetime import datetime as dt

def get_data():
    in_file = 'inputs/day03.test.txt'
    in_file = 'inputs/day03.txt'
    with open(in_file) as f:
        directions = f.readlines()
    turns_array = []
    for line in directions:
        turns = []
        values = line.strip().split(',')
        for val in values:
            turns.append(val)
        turns_array.append(turns)
    return turns_array



def main():
    data = get_data()
    
    d = defaultdict(complex)
    s = defaultdict(complex)
    
    marker = -1j
    for datum in data:
        steps = 0
        marker *= 1j
        z = 0 + 0j
        delta = 0
        for val in datum:
            direction = val[0]
            if direction == 'L':
                delta = -1
            if direction == 'R':
                delta = 1
            if direction == 'U':
                delta = 1j
            if direction == 'D':
                delta = -1j
            num = int(val[1:])
            for i in range(num):
                steps += 1
                z = z + delta
                d[z] += marker
                if (z, marker) not in s:
                    s[(z, marker)] = steps

    distances = []
    steps_needed = []

    for key in d.keys():
        if d[key].real and d[key].imag:
            distances.append(np.abs(key.imag) + np.abs(key.real))
            steps_needed.append(s[(key, 1)] + s[(key, 1j)])
    
    print('Part 1: Minimum Manhattan Distance to crossing is {}'.format(int(min(distances))))
    print('Part 2: Minimum number of steps to a crossing is {}'.format(min(steps_needed)))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
