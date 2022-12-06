import numpy as np
import re
import sys
from collections import Counter
from datetime import datetime as dt


def get_data(is_test=True):
    path = 'inputs/day17.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        line = f.readline()

    pattern = 'target area: x=(\d+)..(\d+), y=(-?\d+)..(-?\d+)'
    x1, x2, y1, y2 = [int(x) for x in re.search(pattern, line).groups()]
    return (x1, x2, y1, y2)

class Target:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    
    def check_in_target(self, pos):
        if pos[0] >= self.x1 and pos[0] <= self.x2 and pos[1] >= self.y1 and pos[1] <= self.y2:
            return True
        return False

    def check_gone_past(self, pos, vel):
        # the starting poition is always above and to the left of the target area. so if y < y_min or x > x_max, then
        # it's not gonna hit the target
        if pos[0] > self.x2 or pos[1] < self.y1:
            return True
        if pos[0] < self.x1 and vel[0] == 0:
            return True
        return False

def take_shot(p1, p2, target):
    pos = np.array([0, 0])
    vel = np.array([p1, p2])
    y_max = pos[0]
    for i in range(2000):
        pos += vel
        if pos[1] > y_max:
            y_max = pos[1]
        vel[0] = np.sign(vel[0]) * (np.abs(vel[0]) - 1)
        vel[1] -= 1
        if target.check_in_target(pos):
            return y_max
        if target.check_gone_past(pos, vel):
            return None


def run(target):
    y_values = []
    velocities = []
    for x_vel in range(0, 2*target.x2):
        for y_vel in range(target.y1*2, 80):
            y_try = take_shot(x_vel, y_vel, target)
            if y_try is not None:
                y_values.append(y_try)
                velocities.append((x_vel, y_vel))
    return max(y_values), len(y_values), velocities
            

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    d = get_data(is_test)
    target = Target(d[0], d[1], d[2], d[3])
    part1, part2, velocities = run(target)
    part1_time = dt.now()
    diff_time = part1_time - begin
    print('Part 1:', part1)
    print('Part 2:', part2)
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #data = get_data(is_test, True)
    #part2 = path_search(data)
    #diff_time = dt.now() - part1_time
    #print('Part 2:', part2)
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
