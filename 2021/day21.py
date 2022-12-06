import numpy as np
import sys
from collections import deque
from datetime import datetime as dt

def get_data(is_test=True):
    start_1 = 4 if is_test else 1
    start_2 = 8 if is_test else 6
    return start_1, start_2

class Die:
    def __init__(self, sides=100):
        self.value = deque(range(1, 1 + sides))
        self.n_rolls = 0
        self.value.rotate()
    def roll(self):
        self.n_rolls += 1
        self.value.rotate(-1)
        return self.value[0]

class Player:
    def __init__(self, label, start_pos, die):
        self.label = label
        self.start_pos = start_pos
        self.space = deque(range(1,11))
        while self.space[0] != start_pos:
            self.space.rotate()
        self.score = 0
        self.die = die
        
    def take_turn(self):
        initial_score = self.score
        initial_space = self.space[0]
        for i in range(3):
            roll = self.die.roll()
            self.space.rotate(-1 * roll)
        self.score += self.space[0]
        # print(self.label, 'from', initial_space, 'to', self.space[0], 'and score from', initial_score, 'to', self.score, 'die rolled', roll)
    
def part1(start_1, start_2):
    die = Die()
    p1 = Player('p1', start_1, die)
    p2 = Player('p2', start_2, die)
    players = deque([p1, p2])
    while p1.score < 1000 and p2.score < 1000:
        players[0].take_turn()
        players.rotate()
    score = players[0].score
    rolls = die.n_rolls
    print(score, rolls, score*rolls)
        
def part2(start_1, start_2):
    die = Die(3)
    p1 = Player('p1', start_1, die)
    p2 = Player('p2', start_2, die)
    players = deque([p1, p2])
    while p1.score < 21 and p2.score < 21:
        players[0].take_turn()
        players.rotate()
    score = players[0].score
    rolls = die.n_rolls
    print(score, rolls, score*rolls)
        
    

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    start_1, start_2 = get_data(is_test)
    part1(start_1, start_2)
    part1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part2(start_1, start_2)
    diff_time = dt.now() - part1_time
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
