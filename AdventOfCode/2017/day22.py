import sys
import numpy as np
import datetime as dt
from collections import defaultdict
from copy import deepcopy

class Virus:
  def __init__(self, mode='original'):
    self.mode = mode
    self.position = 0 + 0j
    self.direction = 0 + 1j
    self.infections_caused = 0
    self.grid = None
  def set_grid(self, grid_dict):
    self.grid = grid_dict
  def burst(self):
    if self.mode == 'original':
      if self.grid[self.position]:
        #already infected, turn right
        self.direction *= -1j
      else:
        # clean, so we'll infect it, and add it to our tally
        self.direction *= 1j
        self.infections_caused += 1
      self.grid[self.position] = 2 - self.grid[self.position]
      self.position += self.direction
    if self.mode == 'evolved':
      # 0 = clean, 1 = weakened, 2 = infected, 3 = flagged
      if self.grid[self.position] == 0:
        self.direction *= 1j
      if self.grid[self.position] == 1:
        self.direction *= 1
        self.infections_caused += 1
      if self.grid[self.position] == 2:
        self.direction *= -1j
      if self.grid[self.position] == 3:
        self.direction *= -1
      self.grid[self.position] = (1 + self.grid[self.position])%4
      self.position += self.direction

  def get_tally(self):
    return self.infections_caused

def main():
  with open('inputs/day22.txt') as f:
    lines = [x.strip() for x in f.readlines()]
    grid = []
    for line in lines:
      grid_line = []
      for l in line:
        if l == '#':
          grid_line.append(2)
        else:
          grid_line.append(0)
      grid.append(grid_line)
    grid = np.array(grid)
    s, s = grid.shape
    center = (s//2, s//2)
    grid_dict = defaultdict(int)
    for i in range(s):
      for k in range(s):
        x = i - center[0]
        y = s - k - center[0]-1
        grid_dict[x +( 1j)*y] = grid[k,i]

    virus = Virus('original')
    virus.set_grid(deepcopy(grid_dict))

    for i in range(10000):
      virus.burst()

    print('Part a: after 10000 bursts, the virus has infected {} nodes'.format(virus.get_tally()))
    
    virus2 = Virus('evolved')
    virus2.set_grid(deepcopy(grid_dict))

    n_bursts = 10000000
    for i in range(n_bursts):
      virus2.burst()
    print('Part b: after {} bursts, the evolved virus has infected {} nodes'.format(n_bursts, virus2.get_tally()))


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

