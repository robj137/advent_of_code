from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np

def get_data(is_test):
    if is_test:
        in_file = 'inputs/day08.test.txt'
    else:
        in_file = 'inputs/day08.txt'
    
    with open(in_file) as f:
        vals = f.read().strip()
    vals = np.array([int(x) for x in list(vals)])

    return vals


def main():
    width = 25
    height = 6
    
    is_test = False
    if len(sys.argv) > 1:
        is_test = True
        width = 2
        height = 2
    
    data = get_data(is_test)
    
    n_layers = int(len(data) / width / height)

    data = np.reshape(data, (n_layers, height, width))
    
    zero_sum = [np.sum(x==0) for x in data]
    min_zero = min(zero_sum)
    layer = zero_sum.index(min(zero_sum))
    n_1 = np.sum(data[layer] == 1)
    n_2 = np.sum(data[layer] == 2)
    part_a = n_1 * n_2

    # this kind of thing seems promising too:
    # mask = (data!=2).argmax(axis=0)
    # this is a 6 x 25 array, where the index is the 
    # layer with the first non-2 value. Need to figure out how to use
    # that info

    pixel_rows = np.array([list('x'*width) for x in range(height)])
    for y in range(height):
        for x in range(width):
            n = 0 # layer number
            color = data[n, y, x]
            while color == 2:
                n += 1
                color = data[n, y, x]
            pixel_rows[y, x] = ' ' if color == 0 else '█'
                
    print('Part 1: {}'.format(part_a))
    print('Part 2: ----------------------------------')
    [print('       ', ''.join(x)) for x in pixel_rows]
    print('------------------------------------------')

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
