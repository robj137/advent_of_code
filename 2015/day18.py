import numpy as np
from datetime import datetime as dt

class grid:
    def __init__(self, data, stuck=False):
        # data is an array of arrays
        # will store this in a numpy array
        data = [y for y in [x for x in data]]
        self.map = np.array(data)
        self.next_map = np.copy(self.map)
        self.stuck_corners = stuck
        if stuck:
            self.set_corners()
    
    def set_corners(self):
        shape = self.map.shape
        for y in range(shape[0]):
            if y == 0 or y == shape[0]-1:
                next_line = ''
                for x in range(shape[0]):
                    next_char = self.map[y][x]
                    if x == 0 or x == shape[0]-1:
                        next_char = '#'
                    next_line += next_char
                self.map[y] = next_line
                        

    def print_map(self):
        print('\n\n\n')
        for line in self.map:
            print((''.join(line)).replace('#','█').replace('.', ' '))                                                             
    def count_lights(self):
        n_lights = 0
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[0]):
                if self.map[i][j] == '#':
                    n_lights += 1
        return n_lights

    def step(self):
        shape = self.map.shape
        for i in range(shape[0]):
            line = ''
            for j in range(shape[0]):
                next_char = '.'
                is_on = True if self.map[i][j] == '#' else False
                n_neighbors_on = self.get_n_neighbors_on(i, j)
                if is_on and n_neighbors_on in [2,3]:
                    next_char = '#'
                if not is_on and n_neighbors_on == 3:
                    next_char = '#'
                line += next_char
            self.next_map[i] = line
        self.map = np.copy(self.next_map)
        if self.stuck_corners:
            self.set_corners()

    def get_n_neighbors_on(self, x, y):
        n_lights = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i == x and j == y:
                    continue
                if i < 0 or j < 0:
                    continue
                if i >= self.map.shape[0] or j >= self.map.shape[0]:
                    continue
                if self.map[i][j] == '#':
                    n_lights += 1
        return n_lights

def get_inputs():
    path = 'inputs/day18.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    return lines

def main():
    get_inputs()

    g = grid(get_inputs())
    g.print_map()

    for i in range(100):
        g.step()
        g.print_map()

    print('Part 1: Number of lights on is {}'.format(g.count_lights()))


    g2 = grid(get_inputs(), stuck=True)
    g2.print_map()

    for i in range(100):
        g2.step()
        g2.print_map()
    print('Part 2: Number of lights with stuck corners is {}'.format(g2.count_lights()))


if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
