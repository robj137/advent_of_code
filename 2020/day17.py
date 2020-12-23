import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re

def print_map(data):
    lines = [''.join(x) for x in data]
    for l in lines:
        print(l)

def get_4data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day17.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day17.txt'
    
    with open(in_file) as f:
        lines = [ np.fromiter(x.strip(), (np.unicode,1)) for x in f.readlines()]
    
    z = w =0
    data = np.array(lines)
    coords = defaultdict(int)
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if data[y][x] == '#':
                coords[(x, y, z, w)] = 1
            else:
                coords[(x,y,z, w)]
    for i in range(-10, 11):
        for j in range(-10, 11):
            for k in range(-6, 7):
                for l in range(-6, 7):
                    coords[(i, j, k, l)]
    return coords

def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day17.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day17.txt'
    
    with open(in_file) as f:
        lines = [ np.fromiter(x.strip(), (np.unicode,1)) for x in f.readlines()]
    
    z = 0
    data = np.array(lines)
    coords = defaultdict(int)
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if data[y][x] == '#':
                coords[(x, y, z)] = 1
            else:
                coords[(x,y,z)]
    for i in range(-10, 11):
        for j in range(-10, 11):
            for k in range(-10, 11):
                coords[(i, j, k)]
    return coords

def examine_neighbors(xyz, coords):
    x, y, z = xyz
    center_val = coords[(x,y,z)]
    n_active = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            for k in [z-1, z, z+1]:
                n_active += coords[(i, j, k)]

    return n_active - center_val

def examine_4dneighbors(xyzw, coords):
    x, y, z, w = xyzw
    center_val = coords[(x,y,z, w)]
    n_active = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            for k in [z-1, z, z+1]:
                for l in [w-1, w, w+1]:
                    n_active += coords[(i, j, k, l)]

    return n_active - center_val

def get_n_active(coords):
    return sum([x for x in coords.values()])

def run(data, is4d=False):
    print(get_n_active(data))   
    run_cycle(data, is4d)
    run_cycle(data, is4d)
    run_cycle(data, is4d)
    run_cycle(data, is4d)
    run_cycle(data, is4d)
    run_cycle(data, is4d)
    print(get_n_active(data))   

def run_cycle(coords, is4d=False):
    print('running a cycle', len(coords))
    
    keys = [x for x in coords.keys()]
    new_value_dict = {}
    for key in keys:
        new_value = None
        if is4d:
            n_active_neighbors = examine_4dneighbors(key, coords)
        else:
            n_active_neighbors = examine_neighbors(key, coords)
        if coords[key] == 1:
            new_value = 1 if n_active_neighbors in [2,3] else 0
        else:
            new_value = 1 if n_active_neighbors ==3 else 0
        new_value_dict[key] = new_value
    for key in new_value_dict:
        coords[key] = new_value_dict[key]


if __name__ == '__main__':
    begin = dt.now()
    m = get_data(False)
    run(m, False)
    m4d = get_4data(False)
    run(m4d, True)
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #p2 = run(data, 30000000)
    #print('Part 2: {}'.format(p2))
    #diff_time = dt.now() - begin
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
