from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
from collections import defaultdict
from intcode import IntCode


def get_data(is_test):
    if is_test:
        in_file = 'inputs/day10.test.txt'
    else:
        in_file = 'inputs/day10.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
        
    map_lines = []
    for y, line in enumerate(lines):
        map_lines.append(list(line))

    asteroid_map = np.array(map_lines)
    return asteroid_map
 
def get_asteroid_dict(asteroid_map):
    asteroids = {}
    shape_y, shape_x = asteroid_map.shape
    for y in range(shape_y):
        for x in range(shape_x):
            if asteroid_map[y,x] == '#':
                asteroids[(x,y)] = defaultdict(int)
    for asteroid_x, asteroid_y in asteroids.keys():
        for x, y in asteroids.keys():
            if x == asteroid_x and y == asteroid_y:
                continue
            elif y == asteroid_y and x != asteroid_x:
                theta = np.pi/2 if x > asteroid_x else -np.pi/2
            else:
                theta = np.arctan((x - asteroid_x) / (y - asteroid_y))
                if asteroid_y < y:
                    theta += np.pi
            asteroids[(asteroid_x, asteroid_y)][theta] += 1
    return asteroids

def part1(asteroids):
    n_asteroids = []
    for key in asteroids:
        n_asteroids.append((len(asteroids[key].keys()), key))
    return max(n_asteroids)
    
def part2(asteroids, base):
    shooting_order_dict = defaultdict(list)
    base_x, base_y = base
    for a_x, a_y in asteroids.keys():
        if base_x == a_x and base_y == a_y:
            continue
        elif a_y == base_y and a_x != base_x:
            theta = np.pi/2 if a_x > base_x else -np.pi/2
        else:
            theta = np.arctan((a_x - base_x) / (-a_y + base_y))
            if base_y > a_y:
                theta += np.pi
        shooting_order_dict[(theta + 3 * np.pi)%(2*np.pi)].append((a_x-base_x, base_y - a_y))        
    
    keys = sorted([x for x in shooting_order_dict.keys()])
    n_keys = 0
    for key in keys:
        n_keys += len(shooting_order_dict[key])

    for key in shooting_order_dict.keys():
        coords = shooting_order_dict[key]
        coords = sorted(coords, key=lambda x: x[0]*x[0] + x[1]*x[1])   
        shooting_order_dict[key] = coords       

    thetas = sorted([x for x in shooting_order_dict.keys()])
    blown = 0
    lucky_200 = None, None
    while shooting_order_dict:
        for theta in thetas:
            if theta in shooting_order_dict and shooting_order_dict[theta]:
                blown += 1
                blown_coords = shooting_order_dict[theta].pop(0)
                bc_x, bc_y = blown_coords
                bc_x1 = bc_x + base_x
                bc_y1 = base_y - bc_y
                if blown == 200:
                    lucky_200 = bc_x1, bc_y1
            else:
                if theta in shooting_order_dict and not shooting_order_dict[theta]:
                    # remove the key
                    del shooting_order_dict[theta]
    part_b = lucky_200[0] * 100 + lucky_200[1]
    return part_b

def main():
 
    is_test = False
    asteroid_map = get_data(is_test)
    asteroids = get_asteroid_dict(asteroid_map)
    
    part_a, base = part1(asteroids)
    part_b = part2(asteroids, base)
    
 

    print('Part 1: {}'.format(part_a))
    print('Part 2: {}'.format(part_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
