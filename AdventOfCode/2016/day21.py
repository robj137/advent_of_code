import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict

def perform_instruction(reg, instr, rev=False):
    instr = instr.split(' ')
    if instr[0] == 'swap':
        a = b = 0
        if instr[1] == 'position':
            a = int(instr[2])
            b = int(instr[5])
        else:
            a = reg.index(instr[2])
            b = reg.index(instr[5])
        reg[a], reg[b] = reg[b], reg[a]
    elif instr[0] == 'reverse':
        a = int(instr[2])
        b = int(instr[4])
        pre = reg[:a]
        post = reg[b+1:]
        mid = [x for x in reversed(reg[a:b+1])]
        temp = pre + mid + post
        for i in range(len(temp)):
            reg[i] = temp[i]
    elif instr[0] == 'rotate' and len(instr) == 4:
        # right -> abcd -> dabc (f.insert(0, f.pop()))
        # left -> abcd -> bcda (f.append(f.pop(0)))
        n_steps = int(instr[2])
        for i in range(n_steps):
            if (not rev and instr[1] == 'left') or (rev and instr[1] == 'right'):
                reg.append(reg.pop(0))
            else:
                reg.insert(0, reg.pop())
    elif instr[0] == 'rotate' and len(instr) == 7:
        # rotate based on position of letter x
        letter = instr[-1]
        if not rev:
            ndx = reg.index(letter)
            n_rots = 1 + ndx
            if ndx >= 4:
                n_rots += 1
            for i in range(n_rots):
                reg.insert(0, reg.pop())
        else:
            orig = reg[:]
            reg.append(reg.pop(0))
            while orig != test_weird_rotate(reg, letter):
                reg.append(reg.pop(0))
    elif instr[0] == 'move':
        a = int(instr[2])
        b = int(instr[5])
        if rev:
            a, b = b, a
        x = reg.pop(a)
        reg.insert(b, x)
    else:
        print('wtf am i even doing?', instr)

def test_weird_rotate(reg, letter):
    ndx = reg.index(letter)
    x = reg[:]
    n_rots = 1 + ndx
    if ndx >= 4:
        n_rots += 1
    for i in range(n_rots):
        x.insert(0, x.pop())
    return x

def get_instructions(test=False):
    path = 'inputs/day21.txt'
    if test:
        path = 'inputs/day21.alt.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    return lines

def part1():
    instructions = get_instructions(True)
    #start = 'abcde'
    start = 'abcdefgh'
    reg = list(start)
    for line in instructions:
        perform_instruction(reg, line)
    
    print('Result of scrambling is {}'.format(''.join(reg)))


def part2():
    instructions = get_instructions(False)
    instructions.reverse()
    start = 'abcde'
    start = 'decab'
    #start = 'abcdefgh'
    start = 'fbgdceah'
    reg = list(start)
    for line in instructions:
        perform_instruction(reg, line, rev=True)
    
    print('Result of (un)-scrambling is {}'.format(''.join(reg)))

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
