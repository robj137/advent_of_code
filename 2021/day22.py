import numpy as np
import re
import sys
import json
from collections import Counter
from datetime import datetime as dt
from copy import deepcopy

def get_data(is_test=True):
    path = 'inputs/day22.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    steps = []
    pattern = '(o\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
        
    for line in lines:
        s = re.search(pattern, line)
        if s:
            g = s.groups()
            steps.append((g[0], [int(x) for x in g[1:]]))

    return steps

def part1(steps):
    # need to convert the ranges from (whatever..whatever) to (-50..50)
    # first truncate, then shift + 50
    lights = np.zeros((101,101,101), dtype=int)
    for action, (x1, x2, y1, y2, z1, z2) in steps:
        x1 = max(x1, -50)
        y1 = max(y1, -50)
        z1 = max(z1, -50)
        x2 = min(x2, 50)
        y2 = min(y2, 50)
        z2 = min(z2, 50)
        if x1 > x2 or y1 > y2 or z1 > z2:
            continue
        x1 += 50
        y1 += 50
        z1 += 50
        x2 += 50
        y2 += 50
        z2 += 50
        setting = 1 if action == 'on' else 0
        lights[x1:x2+1, y1:y2+1, z1:z2+1] = setting

    print(np.sum(lights))

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    steps = get_data(is_test)
    part1(steps)
    
    #run1(nodes1`)
    #part1_time = dt.now()
    #diff_time = part1_time - begin
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #nodes2 = get_data(is_test)
    #run2(nodes2)
    #diff_time = dt.now() - part1_time
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
