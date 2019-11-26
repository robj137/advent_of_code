import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import deque
import heapq

puzzle_input = 'vwbaicqe'
#puzzle_input = 'hijkl'
#puzzle_input = 'kglvqrro'

start = (1,1)
end = (4,4)

dirs_s = ['U', 'D', 'L', 'R']
dirs = [(0,-1), (0, 1), (-1, 0), (1,0)]

def get_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

def get_next_steps(vtx, path, length):
    next_steps = []
    # path is just a string, 'UDULRL'
    h = get_hash(puzzle_input + path)[0:4]
    for i in range(len(h)):
        if int(h[i], 16) > 10: # b, c, d, e, f
            new_vtx = tuple(np.array(vtx) + dirs[i])
            if new_vtx[0] not in [0,5] and new_vtx[1] not in [0,5]:
                new_path = path + dirs_s[i]
                next_steps.append((length + 1, new_path, new_vtx))
    #print(h, vtx, next_steps)
    return next_steps

def get_best_path():
    path = ''
    start_vtx = (0, path, (1,1))
    unvisited = []
    heapq.heappush(unvisited, start_vtx)
    visited = {}
    while unvisited:
        length, path, this_vtx = heapq.heappop(unvisited)
        if this_vtx not in visited:
            visited[(length, path, this_vtx)] = 1
            for new_length, new_path, new_vtx in get_next_steps(this_vtx, path, length):
                if (new_length, new_path, new_vtx) not in visited:
                    heapq.heappush(unvisited, (new_length, new_path, new_vtx))
                    if new_vtx == end:
                        return new_length, new_path, new_vtx
    return -1, 'oops', None

def get_longest_path():
    path = ''
    start_vtx = (0, path, (1,1))
    unvisited = []
    heapq.heappush(unvisited, start_vtx)
    visited = {}
    finished = []
    while unvisited:
        length, path, this_vtx = heapq.heappop(unvisited)
        if this_vtx not in visited:
            visited[(length, path, this_vtx)] = 1
            for new_length, new_path, new_vtx in get_next_steps(this_vtx, path, length):
                if (new_length, new_path, new_vtx) not in visited:
                    if new_vtx != end:
                        heapq.heappush(unvisited, (new_length, new_path, new_vtx))
                    else:
                        finished.append(new_length)
    
    return max(finished)

def part1():
    length, path, vtx = get_best_path()
    print('Part 1: The shortest path is {}'.format(path))

def part2():
    max_path_length = get_longest_path()
    print('Part 2: The longest path length is {}'.format(max_path_length))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
