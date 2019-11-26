import datetime as dt
import numpy as np
from collections import deque

def perform_rule(rule, grid):
  if 'rect' in rule:
    a, b = [int(x) for x in rule.split(' ')[1].split('x')]
    grid[0:b, 0:a] = 1
  if 'rotate' in rule:
    rc, amount = [int(x) for x in rule.split('=')[1].split(' by ')]
    if 'x=' in rule:
      d = deque(grid[:, rc])
      d.rotate(amount)
      grid[:, rc] = d
    else:
      d = deque(grid[rc, :])
      d.rotate(amount)
      grid[rc, :] = d

def draw_grid(grid):
  for line in grid:
    display = ''
    for pixel in line:
      if pixel == 1:
        display += '█'
      else:
        display += ' '
    print(display)

def main():
  with open('inputs/day8.txt') as f:
    rules = [x.strip() for x in f.readlines()]

  grid = np.zeros([6,50])

  for rule in rules:
    perform_rule(rule, grid)

  print('Part a: the number of lights on is {}'.format(np.sum(grid)))
  print('Part b: the pixels spell out:')
  draw_grid(grid)
if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
