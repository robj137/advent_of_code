from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
from collections import defaultdict

class IntCode:
    def __init__(self, program):
        self.switcher = {
            1: self.one,
            2: self.two,
            3: self.three,
            4: self.four,
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine
        }
        self.reset(program)

    def reset(self, program=None):
        if program:
            self.program = program
        self.input = []
        self.output = []
        self.counter = 0
        self.relative_base = 0
        self.params = [0,0,0]
        self.opcode = None
        self.write_index = None
        self.first_arg = None
        self.second_arg = None
        self.waiting = False
        self.finished = False

    def run(self, input_value=None):
        self.waiting = False
        if input_value:
            self.input.append(input_value)
        while not self.finished and not self.waiting:
            self.process_step()
        return self.output
 
    def one(self):
        self.program[self.write_index] = self.first_arg + self.second_arg
        self.counter += 4

    def two(self):
        self.program[self.write_index] = self.first_arg * self.second_arg
        self.counter += 4

    def three(self):
        if not self.input:
            self.waiting = True
            return
        self.program[self.write_index] = self.input.pop(0)
        self.counter += 2

    def four(self):
        self.output.append(self.first_arg)
        self.counter += 2

    def five(self):
        self.counter = self.second_arg if self.first_arg else self.counter + 3

    def six(self):
        self.counter = self.second_arg if not self.first_arg else self.counter + 3

    def seven(self):
        if self.first_arg < self.second_arg:
            self.program[self.write_index] = 1
        else:
            self.program[self.write_index] = 0
        self.counter += 4

    def eight(self):
        if self.first_arg == self.second_arg:
            self.program[self.write_index] = 1
        else:
            self.program[self.write_index] = 0
        self.counter += 4

    def nine(self):
        self.relative_base += self.first_arg
        self.counter += 2
        
    def set_opcode_and_params(self):
        p_code = self.program[self.counter]
        p_code = f'{p_code:05}'
        self.opcode = int(p_code[-2:])
        self.params = [int(x) for x in reversed(p_code[0:3])]
         
        # set first and second arguments
        if self.params[0] == 0:
            self.first_arg = self.program[self.program[self.counter + 1]]
        elif self.params[0] == 1:
            self.first_arg = self.program[self.counter+1]
        elif self.params[0] == 2:
            self.first_arg = self.program[self.program[self.counter + 1] + self.relative_base]
        if self.params[1] == 0:
            self.second_arg = self.program[self.program[self.counter+2]]
        elif self.params[1] == 1:
            self.second_arg = self.program[self.counter+2]
        elif self.params[1] == 2:
            self.second_arg = self.program[self.program[self.counter + 2] + self.relative_base]
        
        # set write index if needed
        #opcodes that do not set a register:
        # 4: 1 arg: self.first_arg arg is either 0, 1, or 2
        # 5,6: 2 args. 1st arg any param, 2nd must be value
        # 9: 1 arg: self.first_arg arg is either 0, 1, or 2

        # opcodes that set a register based on the 3rd parameter
        # 1,2,7,8: 3 args, 1st and 2nd args can be any param, 3 is either 0 or 2
        
        # opcode that sets a register based on 1st parameter
        # 3: 1 arg: self.first_arg arg is 0 or 2
    
        if self.opcode in [1,2,3,7,8]:
            write_par_index = 2 if self.opcode in [1,2,7,8] else 0
            offset = self.relative_base if self.params[write_par_index] == 2 else 0
            self.write_index = self.program[self.counter + write_par_index + 1] + offset
        else:
            self.write_index = None
        
    def process_step(self):
        if self.program[self.counter] == 99:
            self.finished = True
            return
        
        self.set_opcode_and_params()
        func = self.switcher.get(self.opcode)
        return func()

    def set_register(self, address, value):
        self.program[address] = value
