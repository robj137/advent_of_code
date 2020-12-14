import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day14.test.txt'
    else:
        in_file = 'inputs/day14.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    return lines


def divvy_value_into_array(val, length=36):
    if type(val) == str:
        return np.array([int(x) for x in val])
    new_val = np.zeros(length)
    binary_val = format(val, '#038b')[2:]
    binary_val = [int(x) for x in binary_val]
    return np.array(binary_val)

def split_up_mask(mask):
    pass_mask = mask.replace('X', '1')
    and_mask = mask.replace('X', '0')
    return pass_mask, and_mask

def apply_mask(val, mask):
    pass_mask, and_mask = split_up_mask(mask)
    pass_mask = divvy_value_into_array(pass_mask)
    and_mask = divvy_value_into_array(and_mask)
    val = divvy_value_into_array(val)
    c = (val & pass_mask) | and_mask
    return int(''.join([str(x) for x in c]),2)


def get_memory_addresses(mask, addy):
    addy = divvy_value_into_array(addy)
    addy = [str(x) for x in addy]
    for i in range(len(mask)):
        if mask[i] == '1':
            addy[i] = 1
        elif mask[i] == '0':
            addy[i] = addy[i]
        elif mask[i] == 'X':
            addy[i] = 'X'
    addys = [''.join([str(x) for x in addy])]
    while sum(['X' in x for x in addys]) > 0:
        for i in range(len(addys)):
            if 'X' in addys[i]:
                temp_addy = addys.pop(i)
                addys.append(temp_addy.replace('X', '1', 1))
                addys.append(temp_addy.replace('X', '0', 1))
                break
    return addys

def part1(data):
    mem = {}
    mask_pattern = "^mask = ([X10]{36})$"
    mem_pattern = '^mem\[(\d+)\] = (\d+)$'
    mask_re = re.compile(mask_pattern)
    mem_re = re.compile(mem_pattern)
    mask = pass_mask = and_mask = None
    for line in data:
        mask_try = mask_re.search(line)
        mem_try = mem_re.search(line)
        if mask_try:
            mask = mask_try.groups()[0]
            pass_mask, and_mask = split_up_mask(mask)
        elif mem_try:
            memory_address, value = [int(x) for x in mem_try.groups()]
            mem[memory_address] = apply_mask(value, mask)

        else:
            print("WTF")

    value_sum = 0
    for key in mem:
        value_sum += mem[key]
    return value_sum

def part2(data):
    mem = {}
    mask_pattern = "^mask = ([X10]{36})$"
    mem_pattern = '^mem\[(\d+)\] = (\d+)$'
    mask_re = re.compile(mask_pattern)
    mem_re = re.compile(mem_pattern)
    mask = pass_mask = and_mask = None
    for line in data:
        mask_try = mask_re.search(line)
        mem_try = mem_re.search(line)
        if mask_try:
            mask = mask_try.groups()[0]
            pass_mask, and_mask = split_up_mask(mask)
        elif mem_try:
            og_memory_address, value = [int(x) for x in mem_try.groups()]
            memory_addresses = get_memory_addresses(mask, og_memory_address)
            for memory_address in memory_addresses:
                mem[memory_address] = value

        else:
            print("WTF")
    
    value_sum = 0
    for key in mem:
        value_sum += mem[key]
    return value_sum


if __name__ == '__main__':
    begin = dt.now()
    data = get_data(False)
    p1 = part1(data)
    print('Part 1: {}'.format(p1))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    p2 = part2(data)
    print('Part 2: {}'.format(p2))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
