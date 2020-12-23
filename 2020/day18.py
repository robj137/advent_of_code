import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day18.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day18.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
    
    return lines

def perform_calc(calc_array, is_advanced=False):
    if not is_advanced:
        return perform_simple_calc(calc_array)
    else:
        return perform_advanced_calc(calc_array)

def perform_simple_calc(calc_array):
    val = 0
    op = '+'
    for el in calc_array:
        if el in ['*', '+']:
            op = el
        else:
            if op == '+':
                val += el
            else:
                val *= el

    return val

def perform_advanced_calc(calc_array):
    # want to perofrm '+' first.
    while '+'in calc_array:
        ndx = calc_array.index('+')
        new_val = calc_array[ndx-1] + calc_array[ndx+1]
        calc_array[ndx-1] = new_val
        calc_array.pop(ndx)
        calc_array.pop(ndx)

    # there shouldnow be nothing but digits and '*'
    while '*' in calc_array:
        calc_array.pop(calc_array.index('*'))
    
    # and now should just be a simple list of digits that need producted together
    return np.prod(calc_array)

def parse_calc(calc, is_advanced=False):
    # step 1 is to get format the string to only have numbers and +/*
    calc_array = []
    while calc:
        d = calc[0]
        calc = calc[1:]
        if d in [' ', ')']:
            continue
        if d in ['*', '+']:
            calc_array.append(d)
            continue
        new_val = None
        if d.isnumeric():
            # need to check if the next one is numeric too, and so on
            while calc: # just to make sure we dont run off the end
                if calc[0].isnumeric():
                    d += calc[0]
                    calc = calc[1:]
                else:
                    break

            new_val = int(d)
        elif d == '(':
            ndx = find_closing_paranthesis_index(calc)
            sub_calc = calc[:ndx]
            calc = calc[ndx:]
            new_val = parse_calc(sub_calc, is_advanced)
        calc_array.append(new_val)

    # at this point, calc_array should just be a list of ints and '+'s and '*'s
    # for part 1:
    return perform_calc(calc_array, is_advanced)


def find_closing_paranthesis_index(s):
    n_opened = 1 # the firt one
    for i, l in enumerate(s):
        if l == '(':
            n_opened += 1
        if l == ')':
            n_opened -=1
        if n_opened == 0:
            return i

def part1(data):
    s = [parse_calc(x, is_advanced=False) for x in data]
    print(sum(s))

def part2(data):
    s = [parse_calc(x, is_advanced=True) for x in data]
    print(sum(s))

if __name__ == '__main__':
    begin = dt.now()
    part1(get_data(False))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part2(get_data(False))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #p2 = run(data, 30000000)
    #print('Part 2: {}'.format(p2))
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
