from datetime import datetime as dt
import sys
from itertools import permutations
import numpy as np
from collections import defaultdict
from intcode import IntCode
import time

class Arcade:
    def __init__(self, computer):
        self.computer = computer
        self.score = 0
        self.screen = np.zeros((24,42,),dtype=np.str)
        self.ball_x = 0
        self.paddle_x = 0
        self.cheat = False
        self.n_turns = 0
        self.show_turns = False

    def show_score(self):
        print(self.score)

    def get_joystick_input(self):
        self.n_turns += 1
        if self.cheat:
            #naughty, naughty!
            self.computer.input.append(self.ball_x - self.paddle_x)
            return
        direction = input('Input Please')
        val = 0
        if direction in ['l', 'L', 'a']:
            val = -1
        if direction in ['r', 'R', 'd']:
            val = 1
        self.computer.input.append(val)

    def put_a_quarter_in(self):
        self.computer.set_register(0, 2)

    def play(self):
        # run the program cycle
        # print the screen
        # print the score
        # get input
        # feed input into program
        # keep going
        joystick_input = []
        while not self.computer.finished:
            self.computer.output = [] # probably should clear the cache
            output_data = self.computer.run()
            self.print_screen(self.computer.output[:])
            self.get_joystick_input()

    def print_screen(self, output):
            
        stuff = []
        while output:
           stuff.append(output[0:3])
           output = output[3:]
        char_dict = {}
        char_dict[0] = ' '
        char_dict[1] = '+'
        char_dict[2] = '█'
        char_dict[3] = '-'
        char_dict[4] = 'O'
        for el in stuff:
            x, y, z = el
            if x == -1 and y == 0:
                self.score = z
            else:
                self.screen[y,x] = char_dict[z]
            if z == 3: # move the paddle
                self.paddle_x = x
            if z == 4:
                self.ball_x = x
        if self.show_turns:
            print('Score is {}'.format(self.score))
            [print(z) for z in [''.join(y) for y in self.screen]]
            time.sleep(0.01)
   
def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day13.test.txt'
    else:
        in_file = 'inputs/day13.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    program = defaultdict(int)
    for i in range(len(vals)):
        program[i] = vals[i]
    return program
    
def part1(data):
    computer = IntCode(data)
    computer.run()
    stuff = []
    out = computer.output[:]
    while out:
        stuff.append(out[0:3])
        out = out[3:]
    
    game = {}
    for el in stuff:
        x, y, tile = el
        if (x,y) not in game:
            game[(x,y)] = tile
        else:
            if tile == 4 and game[(x,y)] == 2:
                game[(x,y)] = 4
        #if el[2] == 2:
            
    n_blocks = 0
    for key in game:
        if game[key] == 2:
            n_blocks += 1
    return n_blocks

def part2(data):
    computer = IntCode(data)
    arcade = Arcade(computer)
    arcade.cheat = True
    arcade.put_a_quarter_in()
    if len(sys.argv) > 1:
        arcade.show_turns = bool(sys.argv[1])
    arcade.play()
    print('That took {} turns'.format(arcade.n_turns))
    return arcade.score

def main():
 
    is_test = False
    part_a = part1(get_data(is_test))
    part_b = part2(get_data(is_test))
    

    print('Part 1: {}'.format(part_a))
    print('Part 2: {}'.format(part_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
