import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
import heapq

puzzle_input = 1352 #10
destination = (31, 39) #(7,4)

def count_1s(val):
    ones = 0
    for i in val:
        if i == '1':
            ones += 1
    return ones

def is_open(t):
    x, y = t
    val = 2 * x + (x + y) * (x + y + 1)
    
    val += puzzle_input
    if count_1s(bin(val)) % 2 == 1:
        return False
    return True

def get_neighboring_rooms(vtx):
    x, y = vtx
    # assume this is alrady valid.
    valid_rooms = []
    for i in [x - 1, x + 1]:
        if i >= 0 and is_open((i, y)):
            valid_rooms.append((i,y))
    for j in [y - 1, y + 1]:
        if j >= 0 and is_open((x, j)):
            valid_rooms.append((x,j))

    return valid_rooms

def path_search():
    visited = {}
    unvisited = []
    start = (1,1)
    path = str(start)
    p1 = (0, path, start)
    heapq.heappush(unvisited, p1)
    while unvisited:
        length, path, this_vtx = heapq.heappop(unvisited)
        if this_vtx not in visited:
            visited[this_vtx] = 1
            for vtx in get_neighboring_rooms(this_vtx):
                if vtx not in visited:
                    heapq.heappush(unvisited, (length + 1, path + '-' + str(vtx), vtx))
                    if vtx == destination:
                        return length + 1, path, vtx

    return -1, None, None

def part1():
    cost, path, vtx = path_search()
    print('Part 1: cost = {}, path = {}'.format(cost, path))


def part2():
    accessible_in_50 = {}
    visited = {}
    unvisited = []
    start = (1,1)
    p1 = (0, start)
    heapq.heappush(unvisited, p1)
    while unvisited:
        length, this_vtx = heapq.heappop(unvisited)
        if length > 50:
            continue
        if this_vtx not in visited:
            visited[this_vtx] = 1
            accessible_in_50[this_vtx] = 1
            for vtx in get_neighboring_rooms(this_vtx):
                if vtx not in visited:
                    heapq.heappush(unvisited, (length + 1, vtx))
    

    print('Part 2: Number of rooms accessible in 50 or fewer steps is {}'.format(len(accessible_in_50)))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
