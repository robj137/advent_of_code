from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
from collections import defaultdict

class IntCode:
    def __init__(self, program):
        self.reset(program)

    def reset(self, program=None):
        if program:
            self.program = program
        self.input = []
        self.output = []
        self.counter = 0
        self.finished = False
        self.relative_base = 0
        self.waiting = False

    def run(self, input_value=None):
        self.waiting = False
        # will run from the current state until it halts or needs input
        if input_value:
            self.input.append(input_value)
        while not self.finished and not self.waiting:
        #while not self.output and not self.finished:
            self.process_step()
        #if self.output:
        #    return self.output.pop()
        #return None
        return self.output
    
    def process_step(self):
        params = [0,0,0]
        if self.program[self.counter] == 99:
            self.finished = True
            return
        p_code = self.program[self.counter]
        p_code = f'{p_code:05}'
        opcode = int(p_code[-2:])
        params = [int(x) for x in reversed(p_code[0:3])]
        
        
        if params[0] == 0:
            first = self.program[self.program[self.counter + 1]]
        elif params[0] == 1:
            first = self.program[self.counter+1]
        elif params[0] == 2:
            first = self.program[self.program[self.counter + 1] + self.relative_base]
        if params[1] == 0:
            second = self.program[self.program[self.counter+2]]
        elif params[1] == 1:
            second = self.program[self.counter+2]
        elif params[1] == 2:
            second = self.program[self.program[self.counter + 2] + self.relative_base]
            
        offset = self.relative_base if params[2] == 2 else 0


        if opcode == 1:
            self.program[self.program[self.counter+3] + offset] = first + second
            self.counter += 4
        if opcode == 2:
            self.program[self.program[self.counter+3] + offset] = first * second
            self.counter += 4
        if opcode == 3:
            if not self.input:
                self.waiting = True
                return
            an_input = self.input.pop(0)
            if params[0] == 0:
                self.program[self.program[self.counter+1]] = an_input
            elif params[0] == 2:
                self.program[self.program[self.counter+1] + self.relative_base] = an_input
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
                self.program[self.program[self.counter+3] + offset] = 1
            else:
                self.program[self.program[self.counter+3] + offset] = 0
            self.counter += 4
        if opcode == 8: # equals
            if first == second:
                self.program[self.program[self.counter+3] + offset] = 1
            else:
                self.program[self.program[self.counter+3] + offset] = 0
            self.counter += 4

        if opcode == 9: #relative base offset
            self.relative_base += first
            self.counter += 2

