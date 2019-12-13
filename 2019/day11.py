from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
import pandas as pd
from collections import defaultdict
from intcode import IntCode
from matplotlib import pyplot as plt

def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day11.test.txt'
    else:
        in_file = 'inputs/day11.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    program = defaultdict(int)
    for i in range(len(vals)):
        program[i] = vals[i]
    return program
    
def part1(data):
    computer = IntCode(data)
    
    hull = defaultdict(int)
    loc = 0 + 0j
    direction = 1j
    
    input_color = 0 # black
    hull[loc] = input_color
    counter = {}
    while not computer.finished:
        computer.input.append(input_color)
        computer.run()
        # the computer will run, and then add things to their output
        new_color = computer.output[-2]
        new_turn = computer.output[-1]
        hull[loc] = new_color
        counter[loc] = 1
        if new_turn == 0:
            # turn left, multiply by 1j
            direction *= 1j
        else:
            # turn right, multiply by -1j
            direction *= -1j
        loc += direction
        input_color = hull[loc]

    return len(counter)
    
def part2(data):
    computer = IntCode(data)
    
    hull = defaultdict(int)
    loc = 0 + 0j
    direction = 1j
    
    input_color = 1 # whit
    hull[loc] = input_color
    counter = {}
    while not computer.finished:
        computer.input.append(input_color)
        computer.run()
        # the computer will run, and then add things to their output
        new_color = computer.output[-2]
        new_turn = computer.output[-1]
        hull[loc] = new_color
        counter[loc] = 1
        if new_turn == 0:
            # turn left, multiply by 1j
            direction *= 1j
        else:
            # turn right, multiply by -1j
            direction *= -1j
        loc += direction
        input_color = hull[loc]

    pairs = []
    for key in hull:
        if hull[key] == 1:
            pairs.append((key.real, key.imag))
    df = pd.DataFrame(pairs)
    
    # uncommnt below to show using matplotlib
    #df.plot.scatter(x=0, y=1, marker='s')
    #plt.show()
    #input()

    return 'RFEPCFEB'

def main():
 
    is_test = False
    data1 = get_data(is_test)
    part_a = part1(data1)
    part_b = part2(get_data(is_test))
    

    print('Part 1: {}'.format(part_a))
    print('Part 2: {}'.format(part_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
