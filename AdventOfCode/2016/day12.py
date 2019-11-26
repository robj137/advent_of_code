import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict


def get_instructions(test=False):
    path = 'inputs/day12.txt'
    if test:
        path = 'inputs/day12.alt.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    pattern = '([a-z]{3}) (\S{1,2}) ?(\+?\-?\S*)'
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
    step, arg1, arg2 = instructions[ndx]
    # increment ndx now
    ndx += 1
    if step == 'cpy':
        reg = arg2
        val = arg1 if type(arg1) == int else registers_dict[arg1]
        registers_dict[reg] = val
    elif step == 'inc':
        registers_dict[arg1] += 1
    elif step == 'dec':
        registers_dict[arg1] -= 1
    elif step == 'jnz':
        val = arg1 if type(arg1) == int else registers_dict[arg1]
        if val != 0:
            ndx -= 1
            ndx += arg2
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
    instructions = get_instructions(False)
    registers_dict = {'a':0, 'b':0, 'c':0, 'd':0}
    ndx = 0
    while ndx >= 0 and ndx < len(instructions):
        #print(registers_dict, registers_dict['d'] - registers_dict['c'], ndx)
        ndx = take_step(ndx, instructions, registers_dict)
    print('Part 1: The value of register a is {}'.format(registers_dict['a']))


def part2():
    instructions = get_instructions(False)
    registers_dict = {'a':0, 'b':0, 'c':1, 'd':0}
    ndx = 0
    while ndx >= 0 and ndx < len(instructions):
        #print(registers_dict, registers_dict['d'] - registers_dict['c'], ndx)
        ndx = take_step(ndx, instructions, registers_dict)

    print('Part 2: The value of register a is {}'.format(registers_dict['a']))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
