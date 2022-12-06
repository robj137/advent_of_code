import numpy as np
import sys
from collections import deque
import aoc_utils

def get_data(is_test=True):
    path = 'inputs/day25.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = [list(x.strip()) for x in f.readlines()]

    return np.array(lines)
    
def take_step(data):
    m, n = data.shape # so data[m-1, n-1] would be the bottom right most entry
    # first the >
    easties = np.array([x for x in zip(*np.where(data == '>'))])
    desties = np.array([(x, (y+1)%n) for x,y in easties])
    valid = [data[x,y] == '.' for (x,y) in desties]
    easties = easties[valid]
    desties = desties[valid]
    for pair in zip(easties, desties):
        data[tuple(pair[0])], data[tuple(pair[1])] = data[tuple(pair[1])], data[tuple(pair[0])]
    # then the v
    downies = np.array([x for x in zip(*np.where(data == 'v'))])
    desties = np.array([((x+1)%m, y) for x,y in downies])
    valid = [data[x,y] == '.' for (x,y) in desties]
    downies = downies[valid]
    desties = desties[valid]
    for pair in zip(downies, desties):
        data[tuple(pair[0])], data[tuple(pair[1])] = data[tuple(pair[1])], data[tuple(pair[0])]

def visualize(data):
    [print(''.join(x)) for x in data]

def get_string_rep(data):
    return ''.join([''.join(x) for x in data])

@aoc_utils.timer
def part1(data):
    data_s = get_string_rep(data)
    iterated_data_s = ''
    iterations = 0
    while data_s != iterated_data_s:
        iterated_data_s = data_s
        take_step(data)
        iterations += 1
        data_s = get_string_rep(data)

    print(iterations)
        

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
