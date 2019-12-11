from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
from collections import defaultdict
from intcode import IntCode


def get_data(is_test):
    if is_test:
        in_file = 'inputs/day09.test.txt'
    else:
        in_file = 'inputs/day09.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    program = defaultdict(int)
    for i in range(len(vals)):
        program[i] = vals[i]
    return program
    
def main():
 
    is_test = False
    data1 = get_data(is_test)
    data2 = get_data(is_test)
    
    computer1 = IntCode(data1)
    computer2 = IntCode(data2)
    
    part_a = computer1.run(1)
    part_b = computer2.run(2)
    
    print('Part 1: {}'.format(part_a[-1]))
    print('Part 2: {}'.format(part_b[-1]))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
