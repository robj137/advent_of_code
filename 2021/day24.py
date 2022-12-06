import re
import numpy as np
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime as dt
import aoc_utils

class ALU:
    def __init__(self, steps):
        self.steps = steps
        self.registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def set_input(self, input):
        self.registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        self.input = input
        self.str_input = list(str(input))

    def get_input(self):
        #if self.str_input:
        return int(self.str_input.pop(0))

    def operation(self, op, v1, v2):
        var1 = self.registers[v1]
        var2 = self.registers[v2] if v2 in self.registers else int(v2) if v2 is not None else None
        if op == 'inp':
            self.registers[v1] = self.get_input()
        if op == 'add':
            self.registers[v1] += var2
        if op == 'mul':
            self.registers[v1] *= var2
        if op == 'div':
            self.registers[v1] = int(np.floor(self.registers[v1] / var2))
        if op == 'mod':
            self.registers[v1] = self.registers[v1] % var2
        if op == 'eql':
            self.registers[v1] = 1 if self.registers[v1] == var2 else 0
            

    def run(self):
        for step in self.steps:
            print(self.registers)
            self.operation(step[0], step[1], step[2])


def get_data(is_test=False):
    path = 'inputs/day24.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    
    
    pattern = '^(\w+) (\w) ?(-?\w+)?$'
    steps = []
    for line in lines:
        g = re.search(pattern, line).groups()
        steps.append(g)
    return steps

@aoc_utils.timer
def part1(data, trial):
    trial = 11111111111111 if not trial else trial
    alu = ALU(data)
    alu.set_input(trial)
    alu.run()
    print(alu.registers)
    #for i in range(trial-25, trial+25):
    #    alu.set_input(i)
    #    alu.run()
    #    print(i, alu.registers)
    #    if alu.registers['z'] == 0:
    #        print(i)

if __name__ == '__main__':
    data = get_data()
    trial = sys.argv[1] if len(sys.argv) > 1 else None
    part1(data, trial)
