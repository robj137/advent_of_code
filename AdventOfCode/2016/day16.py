import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq

puzzle_input = '00101000101111010'
#puzzle_input = '10000'
fill_length = 272
#fill_length = 20

def step(a):
    b = ''.join(reversed([str(1 - int(x)) for x in a]))
    return a + '0' + b
    #b = [1-x for x in a]
    #b.reverse()
    #return a + [0] + b

def checksum(a, length):
    checksum = a[:length]
    while len(checksum) % 2 == 0:
        checksum = ''.join(['1' if checksum[2*i] == checksum[2*i+1] else '0' for i in range(len(checksum)//2)])
    return checksum

def part(fill_length):
    x = puzzle_input
    while len(x) < fill_length:
        x = step(x)
    return checksum(x, fill_length)



def main():
    this_checksum = part(272)
    print('Part 1: Checksum = {}'.format(this_checksum))
    this_checksum = part(35651584)
    print('Part 2: Checksum = {}'.format(this_checksum))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
