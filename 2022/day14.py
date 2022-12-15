import sys
sys.setrecursionlimit(2000)
import numpy as np
from collections import defaultdict

def parse_structure(line):
    nodes = [np.array(
        [int(y) for y in x.strip().split(',')]) for x in line.split("->")
    ]
    
    this_node = nodes.pop(0)
    structure_blocks = defaultdict(int)
    while nodes:
        next_node = nodes.pop(0)
        vector = next_node - this_node
        vector = vector // np.abs(vector.sum())
        while not (this_node == next_node).all():
            structure_blocks[tuple(this_node)] += 1
            this_node += vector
    structure_blocks[tuple(this_node)] += 1
    return structure_blocks


def get_data():
    with open('inputs/day14.txt') as f:
    #with open('inputs/day14.test.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    blocks = []
    for line in lines:
        blocks.append(parse_structure(line))
    all_blocks = blocks.pop()
    while blocks:
        all_blocks = all_blocks | blocks.pop()
    min_x = min([x for x,y in all_blocks])
    min_y = min([y for x,y in all_blocks])
    max_x = max([x for x,y in all_blocks])
    max_y = max([y for x,y in all_blocks])
    max_y += 1
    delta_x = min_x - 1 - 2*max_y//2
    m = np.full([max_y+2, max_x-min_x+3 + 2*max_y], dtype=str, fill_value=' ')
    for (x, y) in all_blocks:
        m[y, x-delta_x] = '#'
    m[0, 500-delta_x] = '+'
    m[-1:] = '-'
    return m, (0, 500-delta_x)

def print_map(m):
    [print(''.join(x)) for x in m]

def let_one_fall(m, sand_source, true_source):
    ground = 1
    if m[tuple(true_source)] == 'o':
        print_map(m)
        return -1
    pos = np.array(sand_source)
    left = np.array([0, -1])
    right = np.array([0, 1])
    impulse = np.array([1,0])
    while m[tuple(pos + impulse)] == ' ':
        pos += impulse
    
    if m[tuple(pos + impulse)] == '-':
        # we've hit infinity, 
        ground = 0
    if m[tuple(pos+impulse+left)] == ' ':# and m[tuple(pos + left)] == ' ':
        return let_one_fall(m, pos+left, true_source)
    if m[tuple(pos+impulse+right)] == ' ':# and m[tuple(pos + right)] == ' ':
        return let_one_fall(m, pos+right, true_source)
    # no place to go left or right, so here we are
    m[tuple(pos)] = 'o'
    return ground


if __name__ == '__main__':
    m, sand_source = get_data()
    while(let_one_fall(m, sand_source, sand_source)) > 0:
        pass
    uniq, counts = np.unique(m, return_counts=True)
    d = dict(zip(uniq, counts))
    print('Part 1:', d['o'])
    while(let_one_fall(m, sand_source, sand_source)) >-1:
        pass
    uniq, counts = np.unique(m, return_counts=True)
    d = dict(zip(uniq, counts))
    print('Part 2:', d['o'])
