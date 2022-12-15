import sys
import pandas as pd
import numpy as np
import datetime as dt
import re

sys.setrecursionlimit(2000)

def main():
  lines = []
  infile = 'inputs/day17.txt'
  with open(infile) as f:
    lines = [x.strip() for x in f.readlines()]
  
  clay = []
  p1 = 'x=(\d+), y=(\d+)..(\d+)'
  p2 = 'y=(\d+), x=(\d+)..(\d+)'
  for line in lines:
    squares = []
    x_first = True
    parsed = re.search(p1, line)
    if not parsed:
      x_first = False
      parsed = re.search(p2, line)
    a, b, c = [int(x) for x in parsed.groups()]
    for i in range(b, c+1):
      squares.append((a, i))

    if not x_first:
      squares = [(b,a) for a, b in squares]
    clay.extend(squares)
  clay = np.array(list(set(clay)))
  xmin, ymin = np.min(clay, axis=0)
  xmax, ymax = np.max(clay, axis=0)
  print(ymin, ymax, xmin, xmax)

  clay_map = np.zeros([ymax+5, xmax-xmin + 5])
  offset = xmin-2
  clay_map[(ymin, 500-offset)] = 9
  
  for el in clay:    
    y, x = el
    clay_map[(x,y-offset)] = 1
  
  print(clay_map)
 
  vertical_step(clay_map, (ymin, 500-offset))
  print('\n')
  print(clay_map)

  n_tiles_flowing = np.argwhere(clay_map == 2).shape[0]
  n_tiles_standing = np.argwhere(clay_map == 3).shape[0]
  
  print(n_tiles_flowing, n_tiles_standing, n_tiles_flowing + n_tiles_standing)
  print('Part a: All \'wet\' tiles (standing + flowing) = {}'.format(n_tiles_flowing + n_tiles_standing))
  print('Part b: All standing water tiles: {}'.format(n_tiles_standing))
  with open('view.txt', 'w') as f:
    for line in clay_map:
      f.write((''.join([str(int(x)) for x in line])).replace('0', ' ').replace('1','█').replace('2', '~').replace('3', '░') + '\n')



def horizontal_step(m, pos):
  # below was clay or water
  # want to crawl left and right until we come to either
  # a: a clay wall
  # b: a drop (below = 0)
  # should mark as flowing water (2) as cral
  # if we find we're in a basin, turn all the flowing water to standing water (3)
  # eithe way, return the type of origin (2 or 3)
  visited = []
  current = pos[:]
  borders = 0
  while 1:
    # go left
    visited.append(current)
    m[current] = 2 # flowing water
    nxt_down = tuple(np.array(current) + (1, 0))

    if m[nxt_down] == 0:
      # down we go again!
      # nothing more to do except call the vertical step and then break
      down = vertical_step(m, nxt_down)
      if down == 2:
        break
    nxt_pos = tuple(np.array(current) + (0,-1))
    if m[nxt_pos] == 1:
      borders += 1
      break
    current = nxt_pos
  while 1:
    visited.append(current)
    m[current] = 2 # flowing water
    nxt_down = tuple(np.array(current) + (1, 0))

    if m[nxt_down] == 0:
      # down we go again!
      # nothing more to do except call the vertical step and then break
      down = vertical_step(m, nxt_down)
      if down == 2:
        break
    # go right
    nxt_pos = tuple(np.array(current) + (0,1))
    if m[nxt_pos] == 1:
      borders += 1
      break
    current = nxt_pos
  if borders == 2:
    #it's actually standing water!
    for p in visited:
      m[p] = 3 # standing water
    return 3
  return 2

def vertical_step(m, pos):
  # possible node types:
  # just vertical water, only |
  # horizontal push: below is 
  if pos[0] > np.max(np.argwhere(m > 0)[:,0]):
    return 2 #out of bounds, so we don't change the map for this one
  m[pos] = 2 # flowing water
  below_ndx = tuple(np.array(pos) + (1,0))
  below = m[below_ndx]
  if below == 0:
    # perform the vertical step. below might get changed to standing water....
    below = vertical_step(m, below_ndx)
  if below == 1 or below == 3:
    # now we need to do the horizontal step
    this_type = horizontal_step(m, pos)
  return m[pos] # this will get updated to standing water if necessary in the horizontal step

if __name__ == '__main__':
  # 338 too low
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
