import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime as dt
from intcode import IntCode
from collections import defaultdict

def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day02.test.txt'
    else:
        in_file = 'inputs/day02.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    program = defaultdict(int)
    for i in range(len(vals)):
        program[i] = vals[i]
    return program

def compute(data, noun, verb):
    data[1] = noun
    data[2] = verb
    i = 0;
    while data[i] != 99:
        x = data[i+1]
        y = data[i+2]
        placement = data[i+3]
        if data[i] == 1:
            result = data[x] + data[y]
        else:
            result = data[x] * data[y]
        data[placement] = result
        i = i + 4
    return data[0]

def main():
    data = get_data()
    program = data.copy()
    program[1] = 12
    program[2] = 2
    computer = IntCode(program)
    computer.run()
    print('Part 1: {}'.format(computer.program[0]))
    for noun in range(1,100):
        for verb in range(1,100):
            computer.reset(data.copy())
            computer.program[1] = noun
            computer.program[2] = verb
            computer.run()
            if computer.program[0] == 19690720:
                print('Part 2: Noun*100 + Verb = {}'.format(100 * noun + verb))
                return



if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
