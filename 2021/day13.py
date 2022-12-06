import numpy as np
import sys
from collections import Counter
from datetime import datetime as dt

def get_blanket_dimensions(folds):
    found_x = found_y = False
    while not found_x and not found_y:
        for d, index in folds:
            if d == 'x' and not found_x:
                found_x = index
            if d == 'y' and not found_y:
                found_y = index
    return found_x * 2 + 1, found_y * 2 + 1

def get_data(is_test=True):
    path = 'inputs/day13.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    coords = []
    folds = []
    for line in lines:
        if ',' in line:
            x, y = [int(x) for x in line.strip().split(',')]
            coords.append([x, y])
        elif 'fold' in line:
            folds.append(line.split(' ')[-1].split('='))
    coords = np.array(coords)
    
    folds = [[x, int(y)] for x,y in folds]

    max_x, max_y = get_blanket_dimensions(folds)
    blanket = np.zeros([max_y, max_x], dtype=int)
    for x, y in coords:
        blanket[y, x] = 1
    return blanket, folds

def part1(blanket, folds):
    my_blankie = blanket.copy()
    for dimension, index in folds:
        index = int(index)
        if dimension == 'y':
            top = my_blankie[0:index, :]
            bottom = my_blankie[index+1:, :]
            bottom = np.flip(bottom, axis=0)
            my_blankie = top + bottom
        else:
            left = my_blankie[:, 0:index]
            right = my_blankie[:, index + 1:]
            right = np.flip(right, axis=1)
            my_blankie = left + right
        my_blankie[my_blankie > 0] = 1
        print(np.sum(my_blankie))
    
    final = my_blankie.astype('U32')
    final[final == '0'] = ' '
    final[final == '1'] = '█'
    [print(x) for x in [''.join(x) for x in final]]

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    blanket, folds = get_data(is_test)
    part1(blanket, folds)
    part1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    diff_time = dt.now() - part1_time
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
