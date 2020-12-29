import datetime as dt
from collections import Counter, defaultdict, deque
from datetime import datetime as dt
import numpy as np
import re
from copy import deepcopy


def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day24.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day24.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    return [parse_line(x) for x in lines]


def parse_line(line):
    # valid directionals: e, se, sw, w, nw, ne
    directionals = []
    line = list(line[::-1])
    while line:
        direction = line.pop()
        if direction in ['s', 'n']:
            direction += line.pop()
        directionals.append(direction)
    return directionals


def get_dir(label):
    x = y = 0
    if label == 'e':
        x = 1
    elif label == 'se':
        x = 0.5
        y = -0.5
    elif label == 'sw':
        x = -0.5
        y = -0.5
    elif label == 'w':
        x = -1
    elif label == 'nw':
        x = -0.5
        y = 0.5
    elif label == 'ne':
        x = 0.5
        y = 0.5
    return x, y

def find_tile(dirs):
    x = y = 0
    for d in dirs:
        dx, dy = get_dir(d)
        x += dx
        y += dy
    return x, y

def get_neighbor_values(tiles, tile):
    x, y = tile
    neighboring_tiles = [(x-1, y), (x-0.5,y-0.5), (x-0.5, y+0.5), (x+0.5,y+0.5), (x+0.5, y-0.5), (x+1, y)]
    return sum([tiles[x] for x in neighboring_tiles])

def run_round(tiles, write=False):
    tile_keys = [x for x in tiles]
    temp_dict = {}
    for tile in tile_keys:
        neighbors_on = get_neighbor_values(tiles, tile)
        val = tiles[tile]
        if val == 1 and neighbors_on not in [1, 2]:
            val = 0
        elif not val and neighbors_on == 2:
            val = 1
        
        temp_dict[tile] = val
    if write:
        for temp_key in temp_dict:
            tiles[temp_key] = temp_dict[temp_key]





if __name__ == '__main__':
    begin = dt.now()
    is_test = False
    directionals = get_data(is_test)
    tile_dict = defaultdict(int)
    for d in directionals:
        tile = find_tile(d)
        tile_dict[tile] = 1 - tile_dict[tile]

    print('Part 1:', sum(tile_dict.values()))

    part_1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    
    # need to run a "fake" round to pick up the surrounding tiles that aren't keys in the dictionary yet
    # otherwise we wouldn't look at these
    run_round(tile_dict, False)
    
    for i in range(100):
        run_round(tile_dict, True)
    print('Part 2:', sum(tile_dict.values()))
    diff_time = dt.now() - part_1_time
    
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
