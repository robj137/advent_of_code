import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day11.test.txt'
    else:
        in_file = 'inputs/day11.txt'
    
    with open(in_file) as f:

        lines = [ np.fromiter(x.strip(), (np.unicode,1)) for x in f.readlines()]
 
    data = np.array(lines)
    print(data)
    return data


def check_if_valid_point(point, m, n):
    x = point[1]
    y = point[0]
    if x > -1 and y > -1 and x < n and y < m:
        return True
    return False

def run_other_rules(data, indexes, far=False):
    data_new = np.ones_like(data)
    n_cutoff = 4 if not far else 5
    m, n = data.shape

    for j in range(m):
        for i in range(n):
            point = np.array([j, i])
            val = data[point[0], point[1]]
            index = indexes[tuple(point)]
            n_adjacent = np.sum(np.char.count(data[index], '#'))
            
            if val == 'L':
                if n_adjacent == 0:
                    data_new[j, i] = '#'
                else:
                    data_new[j, i] = val
            elif val == '#':
                if n_adjacent >= n_cutoff:
                    data_new[j, i] = 'L'
                else:
                    data_new[j, i] = val
            else:
                data_new[j, i] = val
    return data_new


def print_map(data):
    lines = [''.join(x) for x in data]
    for l in lines:
        print(l)

def get_boolean_indexes_for_one(data, i, j):
    m, n = data.shape
    near = np.zeros(data.shape, dtype=bool)
    far = np.zeros(data.shape, dtype=bool)
    dirs = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    dirs = np.array(dirs)
    near_pairs = []
    far_pairs = []
    point = np.array([j, i])
    for direction in dirs:
        new_point = point + direction
        if check_if_valid_point(new_point, m, n):
            near_pairs.append(tuple(new_point))
    [near.itemset(x, True) for x in near_pairs]
    can_stop = False
    for direction in dirs:
        step = 1
        can_stop = False
        while not can_stop:
            new_point = point + step * direction
            if check_if_valid_point(new_point, m, n):
                if data[new_point[0], new_point[1]] != '.':
                    can_stop = True
                    far_pairs.append(tuple(new_point))
                step += 1
            else:
                can_stop = True
    [far.itemset(x, True) for x in far_pairs]
    return near, far
    
def get_boolean_indexes_for_all(data):
    n, m = data.shape
    near_indexes = {}
    far_indexes = {}
    for j in range(n):
        for i in range(m):
            near, far = get_boolean_indexes_for_one(data, i, j)
            near_indexes[(j, i)] = np.where(near)
            far_indexes[(j, i)] = np.where(far)

    return near_indexes, far_indexes


def run(data, index, far=False):
    data = data.copy()
    while 1:
        #print_map(data)
        new_data = run_other_rules(data, index, far)
        if np.array_equal(data, new_data):
            break
        data = new_data
    return np.sum(np.char.count(data, '#'))

if __name__ == '__main__':
    begin = dt.now()
    #main()
    data = get_data(False)
    near_indexes, far_indexes = get_boolean_indexes_for_all(data)
    diff_time = dt.now() - begin
    print('Getting indexes took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

    part_1_value = run(data, near_indexes, far=False)
    print('Part 1: ', part_1_value)
    part_1_time = dt.now()
    diff_time = part_1_time - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part_2_value = run(data, far_indexes, far=True)
    print('Part 2: ', part_2_value)
    diff_time = dt.now() - part_1_time
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
