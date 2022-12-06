import numpy as np
import sys
from collections import Counter

def get_data(is_test=True):
    path = 'inputs/day11.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    return np.array([[int(x) for x in list(x.strip())] for x in lines])

def step(data):
    M, N = data.shape
    data += 1
    while (data >= 10).any():
        indices = np.transpose(np.where(data >= 10))
        data[data >= 10] = -1000
        for ndx in indices:
            data[max(ndx[0]-1, 0):min(ndx[0]+2, M), max(ndx[1]-1, 0):min(ndx[1]+2, N)] += 1
    n_flashes = np.sum(data < 0)
    data[data < 0] = 0
    return n_flashes
    

def part1(data, n_steps = 10):
    M, N = data.shape
    n_flashes = 0
    for i in range(n_steps):
        n_flashes += step(data)
    print(n_flashes)

def part2(data):
    n = 0
    while np.sum(data == 0) != data.shape[0] * data.shape[1]:
        step(data)
        n += 1
    print(n)

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data.copy(), 100)
    part2(data.copy())
