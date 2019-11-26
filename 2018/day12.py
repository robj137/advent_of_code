import pandas as pd
import numpy as np
import datetime as dt
from collections import Counter

def main():
  states = []
  lines = []
  with open('inputs/day12.txt') as f:
    for line in f:
      if 'initial state' in line:
        initial_state = line.strip().split(': ')[1]
      if '=>' in line:
        lines.append(line.strip())

  # need to expand initial state to incorporate future growth :)
  # depending on how many propagations, this can be added to or removed. 
  # however, for plotting purposes (uncomment out print(state) line below),
  # a smaller padding is nicer.
  # didn't have to build any logic into deciding how big the pads are because part b. is
  # unsolveable by brute force

  begin_pad = 10
  end_pad = 190
  initial_state = '.'*begin_pad + initial_state + '.'*end_pad
  states.append(initial_state)

  grow_dict = {}
  for line in lines:
    key, result = line.split(' => ')
    grow_dict[key] = result

  state = states[-1]
  last_sum = 0
  for i in range(120):
    if i == 20:
      pass #print('Part a: the sum of potted plants is {}'.format(last_sum))
    state = propagate_state(grow_dict, state)
    this_sum = get_sum_of_planted_pots(state, begin_pad)
    diff = this_sum - last_sum
    last_sum = this_sum
    print(state)

  print('So the sum at 120 is {}'.format(this_sum))
  print('We see that things settle down after about 110 or so, with each new generation adding 67')
  left_to_propagate = 50e9 - 120
  total = this_sum + left_to_propagate * diff
  print('Part b: A simple calculation reveals that after 50 billion generations, the sum of planted pots is {}'.format(int(total)))

def get_sum_of_planted_pots(state, begin_pad):
  sums = 0
  for i, pot in enumerate(state):
    if pot == '#':
      sums += i - begin_pad
  return sums

def propagate_state(grow_dict, this_state):
  # kind of hacky for sooo many reasons. strings in python are just like lists, except they're
  # immutable. So hacky temporary replacement of characters to be able to find all indexes of
  # matches. there has to be a better way
  next_state = ['.']*len(this_state)
  for key in grow_dict:
    indices = []
    while key in this_state:
      indices.append(this_state.find(key))
      this_state = list(this_state)
      this_state[indices[-1]] = '!'
      this_state = ''.join(this_state)
    for ndx in indices:
      next_state[ndx+2] = grow_dict[key]
    this_state = this_state.replace('!', key[0])
  return ''.join(next_state)

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
