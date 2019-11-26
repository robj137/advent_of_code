import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict


def get_insructions(test=False):
    path = 'inputs/day23.txt'
    if test:
        path = 'inputs/day23_alt.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    pattern = '([a-z]{3}) ([a-z]?),? ?(\+?\-?\d*)'
    instructions = []
    for line in lines:
        result = re.search(pattern, line)
        if result:
            g = result.groups()
            step = g[0]
            arg = get_int_or_str_or_none(g[1])
            offset = get_int_or_str_or_none(g[2])
            instructions.append((step, arg, offset))
    return instructions

def take_step(ndx, instructions, registers_dict):
    # will return next index
    step, arg, offset = instructions[ndx]
    # increment ndx now
    ndx += 1
    if step == 'inc':
        registers_dict[arg] += 1
    elif step == 'tpl':
        registers_dict[arg] *= 3
    elif step == 'hlf':
        registers_dict[arg] = registers_dict[arg] // 2
    elif step == 'jmp':
        ndx -= 1
        ndx += offset
    elif step == 'jie':
        if registers_dict[arg] % 2 == 0:
            ndx -= 1
            ndx += offset
    elif step == 'jio':
        if registers_dict[arg] == 1:
            ndx -= 1
            ndx += offset
    else:
        print('did not understand instructions')

    return ndx

def get_int_or_str_or_none(t):
    try:
        t = int(t)
        return t
    except:
        pass
    if not t:
        return None
    return t


def part1():
    instructions = get_insructions(False)
    registers_dict = {'a':0, 'b':0}
    ndx = 0
    while ndx >= 0 and ndx < len(instructions):
        ndx = take_step(ndx, instructions, registers_dict)

    print('Part 1: The value of register b is {}'.format(registers_dict['b']))


def part2():
    instructions = get_insructions(False)
    registers_dict = {'a':1, 'b':0}
    ndx = 0
    while ndx >= 0 and ndx < len(instructions):
        ndx = take_step(ndx, instructions, registers_dict)

    print('Part 2: The value of register b is {}'.format(registers_dict['b']))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
