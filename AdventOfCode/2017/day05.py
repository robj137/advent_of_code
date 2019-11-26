import datetime as dt
from collections import Counter

def main():
  offsets = []
  with open('inputs/day5.txt') as f:
    for line in f:
      offsets.append(int(line.strip()))


  offsets = [0,3,0,1,-3]
  index = 0

  offsets_b = offsets[:]
  
  steps = 0
  while index < len(offsets):
    index = take_step(index, offsets)
    steps += 1

  print('Part a: It took {} steps to find the exit'.format(steps))

  steps = 0
  index = 0
  while index < len(offsets_b):
    index = take_weird_step(index, offsets_b)
    steps += 1

  print('Part b: It took {} steps to find the exit'.format(steps))


def take_step(current_index, offsets):
  offset = offsets[current_index]
  offsets[current_index] += 1
  next_index = offset + current_index
  return next_index

def take_weird_step(current_index, offsets):
  offset = offsets[current_index]
  if offset >2:
    offsets[current_index] -= 1
  else:
    offsets[current_index] += 1
  next_index = offset + current_index
  return next_index

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

