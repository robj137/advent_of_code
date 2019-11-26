import pandas as pd
import numpy as np
import datetime as dt
import heapq
import sys

depth = 5616
target = (10,785)
#depth = 510
#target = (10,10)

geologic_index = {(0,0): 0}
erosion_level = {(0,0): depth%20183}
region_index = {(0,0): (depth%20183)%3}

def get_geologic_index(p):
  p = (p[0], p[1])
  if p in geologic_index:
    return geologic_index[p]
  value = 0
  if p == (0,0) or p == target:
    value = 0
  elif p[1] == 0:
    value = p[0] * 16807
  elif p[0] == 0:
    value = p[1] * 48271
  else:
    value = get_erosion_level((p[0]-1,p[1])) * get_erosion_level((p[0], p[1]-1))
  geologic_index[p] = value
  return value

def get_erosion_level(p):
  p = (p[0], p[1])
  if p in erosion_level:
    return erosion_level[p]
  value = (get_geologic_index(p) + depth) % 20183
  erosion_level[p] = value
  region_index[p] = value%3
  return value

def get_region_index(p):
  p = (p[0], p[1])
  if p in region_index:
    return region_index[p]
  return get_erosion_level(p)%3

def get_allowed_flair(p):
  if p[0] < 0 or p[1] < 0:
    return []
  p = (p[0], p[1])
  ri = get_region_index(p)
  flair = ['n', 't', 'c']
  flair.pop(ri) # 
  return flair

def get_neighbors(p):
  neighbors = []
  for direction in [[0,1], [0,-1], [1,0], [-1,0]]:
    new_loc = list(np.array(direction) + np.array([ p[0], p[1]] ) )
    for piece in get_allowed_flair(new_loc):
      if new_loc[0] >= 0 and new_loc[1] >= 0 and piece == p[2]:
        neighbors.append(tuple(new_loc + [piece]))
  for piece in get_allowed_flair(p):
    if piece != p[2]:
      neighbors.append(tuple([p[0], p[1]] + [piece]))
  return neighbors

def get_heuristic(p, tgt):
  # manhattan distance to target from current cell
  return abs(p[0] - tgt[0]) + abs(p[1] - tgt[1])

def path_search(tgt):
  # I guess it's A*? I started with Dijkstra, but modified the heap priority to take into account
  # an heuristic (distance from current cell to the target). This sped up the search from ~ 2
  # minutes to ~ 15 seconds
  p1 = (0,0,'t')
  visited = {}

  heap = []
  heapq.heappush(heap, [0, 0, p1, [p1] ])
  while heap:
    _, path_cost, thisVtxKey, path = heapq.heappop(heap)
    if thisVtxKey not in visited:
      visited[thisVtxKey] = 1
      for vtx in get_neighbors(thisVtxKey):
        if vtx not in visited:
          cost = 1 if vtx[2] == thisVtxKey[2] else 7
          sum1 = path_cost + cost
          heap_cost = sum1 + get_heuristic(vtx, tgt)
          heapq.heappush(heap, [heap_cost, sum1,vtx,path + [vtx]])
          if vtx == tgt:
            return sum1, path, vtx
  return float('inf'), float('inf'), [], [] # didn't work, so return inf

def get_map_character(p):
  if p == (0,0):
    return 'M'
  if p == target:
    return 'T'
  chars = ['.', '=', '|']
  return chars[get_region_index(p)]

def draw_map(M, N):
  #M rows, N columns
  row = ''
  for j in range(M):
    for i in range(N):
      row += get_map_character((i,j))
    row += '\n'
  print(row)

def main():
  danger_level = 0
  for i in range(target[0]+1):
    for j in range(target[1] + 1):
      danger_level += get_erosion_level((i,j))%3

  print('Part a: the total risk level for the smallest rectangle is {}'.format(danger_level))

  #draw_map(16,16)
  minutes, path, vtx = path_search(tuple(list(target)+['t']))
  n_changes = 0
  for i in range(len(path)-1):
    if path[i][0:2] == path[i+1][0:2]:
      n_changes += 1
  x_r, y_r, e_r = zip(*path)
  #print(path)
  print('Part b: it takes {} minutes to reach the reindeer'.format(minutes))
  print('Part b: this included {} steps and {} equipment changes'.format(len(path) - n_changes, n_changes))
  print('Part b: Deepest y was {}, and farthest x was {}'.format(max(y_r), max(x_r)))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
