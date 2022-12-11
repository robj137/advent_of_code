import numpy as np

def get_data():
    #with open('inputs/day10.txt') as f:
    with open('inputs/day10.test.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    return lines

class Device:
    def __init__(self, data):
        self.register = 1
        self.data = data
        self.cycle = 0
        self.instruction_index = -1
        self.current_instruction = 'noop'
        self.current_instruction_lifetime = 0
        self.interesting_signal_strengths = []
        self.crt = []

    def increment_cycle(self):
        # beginning
        self.cycle += 1
        if self.current_instruction_lifetime == 0:
            if self.current_instruction[0:4] == 'addx':
                self.register += int(self.current_instruction.split()[1])
            self.instruction_index += 1
            if self.instruction_index == len(self.data):
                return 0
            self.current_instruction = self.data[self.instruction_index]
            self.current_instruction_lifetime = 1 if self.current_instruction == 'noop' else 2

        # middle bit (during cycle)
        if np.abs((self.cycle-1)%40 - self.register) <= 1:
            self.crt.append('█')
        else:
            self.crt.append(' ')

        self.current_instruction_lifetime -= 1
        if self.cycle in [20, 60, 100, 140, 180, 220]:
            self.interesting_signal_strengths.append(self.cycle * self.register)
        
        return 1

if __name__ == '__main__':
    data = get_data()
    device = Device(data)
    while device.instruction_index < len(device.data):
        device.increment_cycle()

    print('Part 1:', sum(device.interesting_signal_strengths))
    print('Part 2:')
    [print(''.join(x)) for x in np.array(device.crt).reshape(6,40)]
