import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq
import sys

puzzle_input = 5
puzzle_input = 3014603

def part1():

    d = deque([x for x in range(puzzle_input, 0, -1)])
    d.rotate()
    while len(d) > 1:
        d.pop()
        d.rotate()

    print(d)
    return d

def part2(puzzle_input=3014603):


    d = deque([x for x in range(puzzle_input, 0, -1)])
    d.rotate()
    len_d = len(d)
    while len_d > 1:
        d.rotate(len_d // 2 - 1)
        d.pop()
        len_d -= 1
        d.rotate(((len_d-1) // 2))

    if d[0] == puzzle_input:
        print('huzzah', d[0])
    print(puzzle_input, d[0])

def part2_real(x):
    
    samples = [4]
    i = 1
    while samples[-1] < x:
        i += 1
        samples.append(4*samples[-1] - 4)
    samples.pop()
    the_2s = [2**(2*y) for y in range(1,i)]
    if x >= the_2s[-1]:
        print('shiiiit')
        return 'shiiiit'
    ndx = samples[-1] #+ 1
    val = samples[-1] - 1
    print( ndx - (x - val) // 2)
    #print(samples)
    #print(the_2s)


def solve_parttwo():
    left = deque()
    right = deque()
    for i in range(1, puzzle_input+1):
        if i < (puzzle_input // 2) + 1:
            left.append(i)
        else:
            right.appendleft(i)

    while left and right:
        if len(left) > len(right):
            left.pop()
        else:
            right.pop()

        # rotate
        right.appendleft(left.popleft())
        left.append(right.pop())
    return left[0] or right[0]

def main():
    
    part1()
    if len(sys.argv) == 3:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        for i in range(a, b):
            part2(i)

    if len(sys.argv) == 2:
        part2_real(int(sys.argv[1]))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
