from datetime import datetime as dt
import sys
from itertools import permutations
from collections import deque, defaultdict
from intcode import IntCode

def get_program(is_test=False):
    if is_test:
        in_file = 'inputs/day07.test.txt'
    else:
        in_file = 'inputs/day07.txt'
    
    with open(in_file) as f:
        vals = [int(x) for x in f.read().split(',')]
    program = defaultdict(int)
    for i in range(len(vals)):
        program[i] = vals[i]
    return program

def perform_round(program, phases):
    amps = []
    input_signal = 0
    for phase in phases:
        amps.append(IntCode(program.copy()))
        amps[-1].input.append(phase)
    amps = deque(amps)
    while amps:
        amps[0].input.append(input_signal)
        output = amps[0].run()
        if output:
            input_signal = output.pop()
        if amps[0].finished:
            amps.popleft()
        else:
            amps.rotate(-1)
    return input_signal

def main():
    program = get_program(False)
    phase_array = permutations([0,1,2,3,4])
    values = []
    for phases in phase_array:
        values.append((perform_round(program.copy(), phases), phases))
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
