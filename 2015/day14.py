import string
from datetime import datetime as dt
import re
from itertools import permutations

class Reindeer:
    def __init__(self, name, speed, endurance, rest_period):
        self.name = name
        self.speed = speed
        self.endurance_max = endurance
        self.rest_period = rest_period
        self.endurance_left = endurance
        self.rest_left = 0
        self.distance_traveled = 0
        self.points = 0

    def add_point(self):
        self.points += 1

    def get_points(self):
        return self.points

    def get_name(self):
        return self.name

    def get_distance_traveled(self):
        return self.distance_traveled

    def step(self):
        if self.endurance_left:
            self.distance_traveled += self.speed
            self.endurance_left -= 1
            if self.endurance_left == 0:
                # time to rest!
                self.rest_left = self.rest_period
        elif self.rest_left:
            self.rest_left -= 1
            if self.rest_left == 0:
                # done resting!
                self.endurance_left = self.endurance_max

def congratulate_farthest_reindeer(racers):
    farthest = []
    distance = max([r.get_distance_traveled() for r in racers])
    for r in racers:
        if r.get_distance_traveled() == distance:
            r.add_point()
    

def main():
    
    with open('inputs/day14.txt') as f:
        lines = f.readlines()

    pattern = '([A-Z][a-z]+) can fly (\d+) km/s for (\d+) seconds, '
    pattern += 'but then must rest for (\d+) seconds.'
    
    reindeer_racers = []
    for line in lines:
        result = re.search(pattern, line).groups()
        reindeer_racers.append(Reindeer(result[0], 
                                 int(result[1]),
                                 int(result[2]),
                                 int(result[3])))

    for i in range(2503):
        [r.step() for r in reindeer_racers]
        congratulate_farthest_reindeer(reindeer_racers)

    d1 = {}
    d2 = {}
    for r in reindeer_racers:
        d1[r.get_name()] = r.get_distance_traveled()
        d2[r.get_name()] = r.get_points()

    
    print('Part 1: Farthest reindeer got {} km.'.format(max(d1.values())))
    print('Part 2: Most points was {}'.format(max(d2.values())))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
