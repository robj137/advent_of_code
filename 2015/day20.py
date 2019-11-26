import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict


def part1():
    max_house = 1000000
    present_boxes = [0] * max_house
    for i in range(0, max_house):
        elf = i + 1
        n_presents = elf * 10
        house_number = i
        while house_number < max_house:
            present_boxes[house_number] += n_presents
            house_number += elf
    #print(present_boxes)
        if present_boxes[i] > 36000000:
            print('Part 1: First house to break 36 M presents is {}'.format(i+1))
            break

def part2():
    max_house = 1000000
    present_boxes = [0] * max_house
    for i in range(0, max_house):
        elf = i + 1
        n_presents = elf * 11
        house_number = i
        for j in range(50):
            if house_number < max_house:
                present_boxes[house_number] += n_presents
                house_number += elf
        if present_boxes[i] > 36000000:
            print('Part 2: First house with lazy elves to break 36 M is {}'.format(i+1))        
            break

def main():
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
