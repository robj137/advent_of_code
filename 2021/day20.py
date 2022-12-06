import numpy as np
import re
import sys
import json
from collections import Counter
from datetime import datetime as dt
from copy import deepcopy

def get_data(is_test=True):
    path = 'inputs/day20.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        algo = f.readline().strip()
        f.readline()
        pic = np.array([[int(x) for x in list(y.strip().replace('.', '0').replace('#', '1'))] for y in f.readlines()])

    pm, pn = pic.shape
    # for now, let's pad by 5
    pad = 53
    m = pm + 2 * pad
    n = pn + 2 * pad
    image = np.zeros([m, n], int)
    image[pad:pad+pm, pad:pad+pn] = pic
    image = image.astype('U16')
    image[image=='1'] = '#'
    image[image=='0'] = '.'
    return algo, image

def enhance(image, algo):
    m, n = image.shape
    new_image = image.copy()
    for i in range(1, m-1):
        for j in range(1, n-1):
            sub_image = image[i-1:i+2,j-1:j+2]
            key = int(''.join([''.join(x) for x in sub_image]).replace('.', '0').replace('#', '1'),2)
            new_image[i, j] = algo[key]
    if algo[0] == '#':
        new_image[0, :] = new_image[1,1]
        new_image[m-1, :] = new_image[1,1]
        new_image[:, 0] = new_image[1,1]
        new_image[:, n-1] = new_image[1,1]
    return new_image

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    algo, pic = get_data(is_test)
    for i in range(50):
        [print(''.join(x)) for x in pic]
        print()
        pic = enhance(pic, algo)
    [print(''.join(x)) for x in pic]
    print(Counter(''.join([''.join(x) for x in pic]))['#'])
    #run1(nodes1`)
    #part1_time = dt.now()
    #diff_time = part1_time - begin
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #nodes2 = get_data(is_test)
    #run2(nodes2)
    #diff_time = dt.now() - part1_time
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
