import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day08.test.txt'
    else:
        in_file = 'inputs/day08.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
 
    return lines



def part1():
    data = get_data(False)
    data.append('brk 0')
    instructions_performed = {}
    index = 0
    acc = 0
    while 1:
        if index in instructions_performed:
            break
        instructions_performed[index] = 0
        instruction, val = data[index].split(' ')
        #print(index, instruction, val, acc)
        if instruction == 'nop':
            index += 1
        if instruction == 'acc':
            acc += int(val)
            index += 1
        if instruction == 'jmp':
            index += int(val)
        if instruction == 'brk':
            break


    print(acc)


def trial(data, i):
    trial_data = data[:]
    row = trial_data[i]
    if 'nop' in row:
        trial_data[i] = row.replace('nop', 'jmp')
    elif 'jmp' in row:
        trial_data[i] = row.replace('jmp', 'nop')
    else:
        return False
    instructions_performed = {}
    index = 0
    acc = 0
    while 1:
        if index in instructions_performed:
            return False
        instructions_performed[index] = 0
        instruction, val = trial_data[index].split(' ')
        #print(index, instruction, val, acc)
        if instruction == 'nop':
            index += 1
        if instruction == 'acc':
            acc += int(val)
            index += 1
        if instruction == 'jmp':
            index += int(val)
        if instruction == 'brk':
            return acc


def part2():
    data = get_data(False)
    data.append('brk 0')
    for i in range(len(data)):
        something = trial(data, i)
        if something:
            print(something)

def main():
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    #main()
    part1()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part2()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
