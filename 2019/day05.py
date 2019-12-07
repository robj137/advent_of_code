from datetime import datetime as dt
import sys

def get_data():
    in_file = 'inputs/day05.test.txt'
    in_file = 'inputs/day05.txt'
    with open(in_file) as f:
        values = [int(x) for x in f.read().split(',')]
    return values


def process(data, io):
    input_value = io[0]
    i = 0;
    j = 0
    params = [0,0,0]
    while i < len(data):
        j += 1
        if data[i] == 99:
            break
        p_code = data[i]
        p_code = f'{p_code:05}'
        opcode = int(p_code[-2:])
        params = [int(x) for x in reversed(p_code[0:3])]
        
        first = data[i+1] if params[0] else data[data[i+1]]
        second = data[i+2] if params[1] else data[data[i+2]] if len(data) > data[i+2] else None
        
        if opcode == 1:
            data[data[i+3]] = first + second
            i += 4
        if opcode == 2:
            data[data[i+3]] = first * second
            i += 4
        if opcode == 3:
            data[data[i+1]] = input_value
            i += 2
        if opcode == 4:
            io[1].append(first)
            i += 2
        if opcode == 5: # jump-if-true
            i = second if first else i + 3
        if opcode == 6: # jump-if-false
            i = second if not first else i + 3
        if opcode == 7: # less than
            if first < second:
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0
            i += 4
        if opcode == 8: # equals
            if first == second:
                data[data[i+3]] = 1
            else:
                data[data[i+3]] = 0
            i += 4
        
    return io[1]

def main():
    data = get_data()
    
    io1 = [1, []]
    io2 = [5, []]
    
    process(data[:], io1)
    process(data[:], io2)
    print('Part 1: {}'.format(io1[1][-1]))
    print('Part 2: {}'.format(io2[1][-1]))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
