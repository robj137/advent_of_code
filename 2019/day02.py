import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime as dt

def get_data():
    in_file = 'inputs/day02.test.txt'
    in_file = 'inputs/day02.txt'
    with open(in_file) as f:
        lines = f.read()
    return [int(x) for x in lines.split(',')]


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
    part_1_answer = compute(data[:], 12, 2)
    print('Part 1: {}'.format(part_1_answer))

    for noun in range(1,100):
        for verb in range(1,100):
            if compute(data[:], noun, verb) == 19690720:
                print('Part 2: Noun*100 + Verb = {}'.format(100 * noun + verb))
                return



if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
