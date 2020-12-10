import datetime as dt
from collections import Counter
from datetime import datetime as dt
import numpy as np

def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day03.test.txt'
    else:
        in_file = 'inputs/day03.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
        
    map_lines = []
    for y, line in enumerate(lines):
        map_lines.append(list(line))

    tree_map = np.array(map_lines)
    return tree_map

def do_run(data, row_skip, pos_skip):
    x_pos = 0
    y_pos = 0
    height, width = data.shape
    trees_hit = 0
    for row in range(row_skip, height, row_skip):
        x_pos = (x_pos + pos_skip) % width
        if data[row, x_pos] == '#':
            trees_hit += 1
    return trees_hit

def main():
    data = get_data(is_test=False)
    trees_hit = do_run(data, 1, 3)
    runs = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    trees_hit = []
    for pos_skip, row_skip in runs:
        trees_hit.append(do_run(data, row_skip, pos_skip))
    print(trees_hit)
    print(np.prod(trees_hit))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
