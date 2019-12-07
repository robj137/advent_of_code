from datetime import datetime as dt
import sys
from itertools import permutations
from collections import deque

class Amplifier:
    def __init__(self, program, phase_factor):
        self.program = program
        self.phase_factor = [phase_factor]
        self.input = []
        self.output = []
        self.counter = 0
        self.finished = False

    def turn_crank(self, input_value):
        self.input.append(input_value)
        while not self.output and not self.finished:
            self.process_step()
        if self.output:
            return self.output.pop()
        return None

    def process_step(self):
        params = [0,0,0]
        if self.program[self.counter] == 99:
            self.finished = True
            return
        p_code = self.program[self.counter]
        p_code = f'{p_code:05}'
        opcode = int(p_code[-2:])
        params = [int(x) for x in reversed(p_code[0:3])]
        first = self.program[self.counter+1] if params[0] else self.program[self.program[self.counter+1]]
        second = self.program[self.counter+2] if params[1] else self.program[self.program[self.counter+2]] if len(self.program) > self.program[self.counter+2] else None
        
        if opcode == 1:
            self.program[self.program[self.counter+3]] = first + second
            self.counter += 4
        if opcode == 2:
            self.program[self.program[self.counter+3]] = first * second
            self.counter += 4
        if opcode == 3:
            an_input = None
            if self.phase_factor:
                an_input = self.phase_factor.pop()
            else:
                an_input = self.input.pop()
            self.program[self.program[self.counter+1]] = an_input
            self.counter += 2
        if opcode == 4:
            self.output.append(first)
            self.counter += 2
        if opcode == 5: # jump-if-true
            self.counter = second if first else self.counter + 3
        if opcode == 6: # jump-if-false
            self.counter = second if not first else self.counter + 3
        if opcode == 7: # less than
            if first < second:
                self.program[self.program[self.counter+3]] = 1
            else:
                self.program[self.program[self.counter+3]] = 0
            self.counter += 4
        if opcode == 8: # equals
            if first == second:
                self.program[self.program[self.counter+3]] = 1
            else:
                self.program[self.program[self.counter+3]] = 0
            self.counter += 4
        
def get_program():
    in_file = 'inputs/day07.test.txt'
    in_file = 'inputs/day07.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    return vals

def perform_round(program, phases):
    amps = []
    input_signal = 0
    for phase in phases:
        amps.append(Amplifier(program[:], phase))
    amps = deque(amps)
    while amps:
        output = amps[0].turn_crank(input_signal)
        if output:
            input_signal = output
        if amps[0].finished:
            amps.popleft()
        else:
            amps.rotate(-1)
    return input_signal

def main():
    program = get_program()
    phase_array = permutations([0,1,2,3,4])
    values = []
    for phases in phase_array:
        values.append((perform_round(program[:], phases), phases))
    part_a = max(values)[0]
    
    phase_array = permutations([5,6,7,8,9])
    values = []
    for phases in phase_array:
        values.append((perform_round(program, phases), phases))
    part_b = max(values)[0]

    print('Part 1: {}'.format(part_a))
    print('Part 2: {}'.format(part_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
