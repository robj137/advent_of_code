import numpy as np
import sys
import re
from collections import defaultdict

class Brood:
    def __init__(self, days_left):
        self.days_left = days_left
        self.number = 0
        self.immature_number = 0
        self.new_spawn = 0

    def increment(self):
        if self.days_left != 0:
            self.days_left -= 1
        else:
            self.new_spawn = self.number
            self.number += self.immature_number
            self.immature_number = 0
            self.days_left = 6

class School:
    def __init__(self, initial_fishies):
        self.broods = [
            Brood(0),
            Brood(1),
            Brood(2),
            Brood(3),
            Brood(4),
            Brood(5),
            Brood(6)
        ]
        for fish in initial_fishies:
            self.broods[fish].number += 1

    def increment(self):
        new_spawn = 0
        for brood in self.broods:
            brood.increment()
            new_spawn += brood.new_spawn
            brood.new_spawn = 0

        nursery = [x for x in filter(lambda x: x.days_left == 1, self.broods)][0]
        nursery.immature_number = new_spawn

    def get_fish_ages(self):
        return [x for x in map(lambda x: '{}:{}'.format(x.days_left, x.number), self.broods)]
    
    def get_fish_totals(self):
        return sum(map(lambda x: x.number + x.immature_number, self.broods))

def get_data(is_test=True):
    path = 'inputs/day06.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        fishies = f.read()

    fishies = [int(x) for x in fishies.strip().split(',')]
    return fishies

def part1(fishies):
    school = School(fishies)
    for i in range(1, 257):
        school.increment()
        print(i, school.get_fish_totals(), school.get_fish_ages())

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
