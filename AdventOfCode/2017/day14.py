import datetime as dt
import re
import numpy as np
from collections import defaultdict, Counter, deque
import operator

def reverse(l, n):
  # assumes start at 0
  for i in range(int(n/2)):
    l[i], l[n-i-1] = l[n-i-1], l[i]

def run_round(numbers, lengths, current_position, skip_size):
  n_rotations = current_position
  numbers.rotate(-n_rotations)
  for length in lengths:
    reverse(numbers, length)
    numbers.rotate(-length - skip_size)
    n_rotations += length + skip_size
    skip_size += 1

  current_position = n_rotations%len(numbers)
  numbers.rotate(n_rotations)
  return current_position, skip_size

def convert_sparse_to_dense(numbers):
  numbers = list(numbers)
  dense_hash = ''
  while numbers:
    block = numbers[0:16]
    numbers = numbers[16:]
    current = 0
    for number in block:
      current = current ^ number
    dense_hash+=('{0:#04x}'.format(current)[-2:])
  return dense_hash

def get_knot_hash_binary(s):
  s = [ord(x) for x in s ]
  s.extend([17,31,73,47,23])
  numbers = deque([x for x in range(256)])
  current_position = 0
  skip_size = 0
  for _ in range(64):
    current_position, skip_size = run_round(numbers, s, current_position, skip_size)
  
  dense_hash = '0x'+convert_sparse_to_dense(numbers)
  b = ''
  for c in dense_hash[2:]:
    b += '{0:#06b}'.format(int('0x'+c,16))[2:]
  return b

def main():
  puzzle_input = 'hxtvlmkl'
  #puzzle_input = 'flqrgnkx'

  sums = 0
  lines = []
  for i in range(128):
    s = '{}-{}'.format(puzzle_input, i)
    b = get_knot_hash_binary(s)
    lines.append(b)
    #sums += get_knot_hash_ones_count(s)

  grid = np.array([[int(y) for y in x] for x in lines])
  
  digit_map = {}

  n_squares= 0
  for x in range(grid.shape[0]):
    for y in range(grid.shape[1]):
      if grid[x,y]:
        n_squares += 1
        digit_map[(x,y)] = []
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
        for dx, dy in neighbors:
          if check_inbounds(dx, dy, grid):
            if grid[dx, dy]:
                digit_map[(x,y)].append((dx, dy))

  print('Part a: Number of squares used: {}'.format(n_squares))

  groups = []
  while digit_map:
    group = []
    key = [x for x in digit_map.keys()][0]
    crawl_and_grab(key, group, digit_map)
    
    groups.append(group)

  print('Part b: Number of distinct groups: {}'.format(len(groups)))
    

def crawl_and_grab(key, group, digit_map):
  #print('digit map length: {}'.format(len(digit_map)))
  group.append(key)
  friends = digit_map[key]
  del digit_map[key]
  for n in friends:
    if n in digit_map:
      crawl_and_grab(n, group, digit_map)

def check_inbounds(x,y, grid):  
  return not (x < 0 or y < 0 or x>= grid.shape[0] or y>= grid.shape[1])
  


if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

