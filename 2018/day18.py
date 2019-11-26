import pandas as pd
import numpy as np
import datetime as dt
from collections import Counter

def prettify_map(landscape):
  print('')
  for line in landscape:
    print(''.join(line))

def apply_rule(i, j, landscape):
  typ = landscape[i,j]
  val = typ
  if typ == '.': # open
    if np.argwhere(landscape[max(i-1, 0):min(i+2, len(landscape)+1), max(j-1, 0):min(j+2, len(landscape)+1)]=='|').shape[0] >= 3:
      val = '|'
  if typ == '|': # treee
    if np.argwhere(landscape[max(i-1, 0):min(i+2, len(landscape)+1), max(j-1, 0):min(j+2, len(landscape)+1)]=='#').shape[0] >= 3:
      val = '#'
  if typ == '#': # lumberyard
    val = '.'
    if np.argwhere(landscape[max(i-1, 0):min(i+2, len(landscape)+1), max(j-1, 0):min(j+2, len(landscape)+1)]=='#').shape[0] >= 2:
      if np.argwhere(landscape[max(i-1, 0):min(i+2, len(landscape)+1), max(j-1, 0):min(j+2, len(landscape)+1)]=='|').shape[0] > 0:
        val = '#'
  return val

def transform(landscape):
  xformed = landscape.copy()
  for i in range(len(landscape)):
    for j in range(len(landscape[i])):
      xformed[i, j] = apply_rule(i, j, landscape)
  return xformed

def get_resource_value(landscape):
  n_trees = np.argwhere(landscape=='|').shape[0]
  n_yards = np.argwhere(landscape=='#').shape[0]
  return n_trees * n_yards

def main():
  landscape = []
  with open('inputs/day18.txt') as f:
    for line in f:
      landscape.append([x for x in line.strip()])

  landscape = np.array(landscape)
  value = 0
  values = []
  for i in range(1500):
    landscape = transform(landscape)
    values.append(get_resource_value(landscape))
    #prettify_map(landscape)

  # our hunch is that there's a cyclical nature in the resource values. Looking at the 
  # plot of the landscape as the minutes goes by makes it seem like this is a good hunch
  # so we take enough samples so that we think we have captured several cycles
  # then we bin the values and look the highest value(s). Then we make a cutoff of, say, half that value
  # and look for the number of values that ar ein the cycle (cycle_length)
  c = Counter(values)
  hits = c.most_common(1)[0][1]
  cycle_length = 0
  for key in c.keys():
    if c[key] > hits/2:
      cycle_length += 1

  # now we know the cycle length, so it's just a matter of finding what th eremainder from 10^lots is
  # and grabbing a value that we think is the same divmod cycle_length
  d, r = divmod(1000000000, cycle_length)
  while r < 1000:
    r += cycle_length

  print('Part b: the value after 1000000000 minutes will be {}'.format(values[r-1]))


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
