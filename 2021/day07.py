import numpy as np
import sys
import re
from collections import defaultdict

def get_data(is_test=True):
    path = 'inputs/day07.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        positions = f.read()

    positions = [int(x) for x in positions.strip().split(',')]
    return positions

def get_cost(x):
  cost = x * (x+1) / 2
  return x * (x+1) / 2


def part1(data):
    m1 = min(data)
    m2 = max(data)
    data = np.array(data)
    best = 1000000000000000000000
    best_index = 100000000000000000000000
    for i in range(m1, m2+1):
        trial = sum([get_cost(abs(i - x)) for x in data])
        if trial < best:
            best = trial
            best_index = i
    print(best_index, best)


if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
