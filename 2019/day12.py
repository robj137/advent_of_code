from datetime import datetime as dt
import sys
import numpy as np
import re
from collections import deque, Counter


class Moon:
    def __init__(self, coord, name):
        self.position = np.array([coord[0], coord[1], coord[2]])
        self.velocity = np.array([0, 0, 0])
        self.name = name

    def take_step(self):
        self.position += self.velocity

    def print_state(self):
        msg = 'pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>'
        msg = msg.format(
                        self.position[0],
                        self.position[1],
                        self.position[2],
                        self.velocity[0],
                        self.velocity[1],
                        self.velocity[2])
        return msg

    def get_potential_energy(self):
        return sum(np.abs(self.position))

    def get_kinetic_energy(self):
        return sum(np.abs(self.velocity))
        
    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

def get_data(is_test):
    if is_test:
        in_file = 'inputs/day12.test.txt'
    else:
        in_file = 'inputs/day12.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
 
    pattern = '<x=(-?\d+), y=(-?\d+), z=(-?\d+)>'
    coords = []
    for line in lines:
        s = re.search(pattern, line)
        if s:
            g = s.groups()
            coords.append([int(x) for x in g])
    return coords
 
def part2(data):
    return None

def take_step(moons):
    for i in range(4):
        moon = moons[0]
        for j in range(1,4):
            next_moon = moons[j]
            # only calculate one way! no double counting!
            moon.velocity[moon.position < next_moon.position] += 1
            moon.velocity[moon.position > next_moon.position] += -1
        moons.rotate(-1)
    for moon in moons:
        moon.position += moon.velocity

def get_prime_factors(n):
    factors = []
    for i in range(2, int(n/2+ 1)):
        while n%i == 0:
            factors.append(i)
            n = n // i
    return factors


def get_lcm(vals):
    factors = [get_prime_factors(x) for x in vals]
    lcm_dict = {}
    for factor in factors:
        c = Counter(factor)
        for x in c:
            if x not in lcm_dict:
                lcm_dict[x] = c[x]
            else:
                if c[x] > lcm_dict[x]:
                    lcm_dict[x] = c[x]
    lcm = 1
    for key in lcm_dict:
        for i in range(lcm_dict[key]):
            lcm *= key
    return lcm

def main():
 
    is_test = False
    data = get_data(is_test)
    moon_names = ['Io', 'Europa', 'Ganymede', 'Callisto']
    moons = []
    for i in range(len(moon_names)):
        moons.append(Moon(data[i], moon_names[i]))

    moons = deque(moons)


    for i in range(1000):
        take_step(moons)

    energy = 0
    for moon in moons:
        #print(moon.print_state())
        energy += moon.get_total_energy()
        #print(moon.get_total_energy())

    part_a = energy
    
    initial_pos_x = np.array([moon.position[0] for moon in moons])
    initial_pos_y = np.array([moon.position[1] for moon in moons])
    initial_pos_z = np.array([moon.position[2] for moon in moons])
    initial_vel_x = np.array([moon.velocity[0] for moon in moons])
    initial_vel_y = np.array([moon.velocity[1] for moon in moons])
    initial_vel_z = np.array([moon.velocity[2] for moon in moons])

    
    cycles = []
    step = 0
    while len(cycles) < 3:
        take_step(moons)
        step += 1
        pos_x = np.array([moon.position[0] for moon in moons])
        vel_x = np.array([moon.velocity[0] for moon in moons])
        pos_y = np.array([moon.position[1] for moon in moons])
        vel_y = np.array([moon.velocity[1] for moon in moons])
        pos_z = np.array([moon.position[2] for moon in moons])
        vel_z = np.array([moon.velocity[2] for moon in moons])
        if (pos_x == initial_pos_x).all() and (vel_x == initial_vel_x).all():
            cycles.append(step)
            initial_pos_x = np.array([0,0,0,0])
        if (pos_y == initial_pos_y).all() and (vel_y == initial_vel_y).all():
            cycles.append(step)
            initial_pos_y = np.array([0,0,0,0])
        if (pos_z == initial_pos_z).all() and (vel_z == initial_vel_z).all():
            cycles.append(step)
            initial_pos_z = np.array([0,0,0,0])


    print('Part 1: {}'.format(part_a))
    print('Part 2: {}'.format(get_lcm(cycles)))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
