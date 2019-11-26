import datetime as dt
from collections import deque
import numpy as np

config_dict = {}

def main():
  counts = []
  with open('inputs/day6.txt') as f:
    counts = [int(x) for x in f.readline().strip().split()]

  counts = deque(counts)
  config_dict[tuple(counts)] = 0
  
  steps = 0
  start = -1
  while(1):
    cycle(counts)
    steps += 1
    if tuple(counts) in config_dict:
      start = config_dict[tuple(counts)]
      break
    else:
      config_dict[tuple(counts)] = steps

  print('Part a: It took {} steps to find a duplicate configuration'.format(steps))
  print('Part b: There are {} cycles in the infinite loop.'.format(steps-start))
  
def cycle(counts):
  ndx = np.argmax(counts) 
  counts.rotate(-ndx)
  wealth = counts[0]
  counts[0] = 0
  i = 1
  
  while wealth:
    counts[i%len(counts)] += 1
    wealth -= 1
    i += 1

  counts.rotate(ndx)

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

