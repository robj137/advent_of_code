import numpy as np
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime as dt
import aoc_utils


def get_data(is_test=True):
    path = 'inputs/day23.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = [list(x)[:-1] for x in f.readlines()]
    
    
    return np.array(lines)

class Hallway:
    def __init__(self, data):
        self.data = data.copy()
        self.walls = np.where(data == '#')
        self.parking_spots = [(1,1), (1,2), (1,4), (1,6), (1,8), (1,10), (1,11)]
        [self.a1, self.a2] = [(x,y) for x, y in zip(*np.where(data=='A'))]
        [self.b1, self.b2] = [(x,y) for x, y in zip(*np.where(data=='B'))]
        [self.c1, self.c2] = [(x,y) for x, y in zip(*np.where(data=='C'))]
        [self.d1, self.d2] = [(x,y) for x, y in zip(*np.where(data=='D'))]
        self.home_base = {
            'A': [(2,3), (3,3)],
            'B': [(2,5), (3,5)],
            'C': [(2,7), (3,7)],
            'D': [(2,9), (3,9)],
        }

class Amphipod:
    def __init__(self, hallway, initial_loc):
        self.initial_loc = initial_loc
        self.pos = initial_loc
        self.hallway = hallway
        self.type = hallway.data[initial_loc]
        self.set_move_cost()

    def is_home(self):
        if self.pos not in self.hallway.home_base[self.type]:
            return False
        if self.pos[0] == 3:
            return True # it's in the home base and lowest
        if self.hallway.data[self.pos[0]+1, self.pos[1]] == self.type:
            return True
        return False

    def set_move_cost(self):
        d = {'A': 1, 'B': 10, 'C':100, 'D':1000}
        self.move_cost = d[self.type]

    def get_distance(self, loc):
        diff = loc-pos
        return abs(diff[0]) + abs(diff[1])

    def get_available_moves(self):
        

@aoc_utils.timer
def part1(data):
    print(data)
    pass

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
