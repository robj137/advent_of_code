import pickle
import numpy as np
import datetime as dt
from collections import defaultdict
import heapq
import sys
import random

n_crawls = 0

def main():
  with open('inputs/day20.test2.txt') as f:
    dirs = f.read()


  #dirs = '^E(E|NN|W)$'
  #dirs = '^W(W|N)$'
  #dirs = '^WNE$'
  #dirs = '^ENWWW(NEEE|SSE(EE|N))$'
  #dirs = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
  #dirs = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'
  #dirs = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
  base_map = defaultdict(list)
  current_room = (0,0)
  branch_queue = [[0,len(dirs)-1, len(dirs)-1]]
  print(dirs)
  follow_nodes(dirs, branch_queue, base_map, current_room)
  get_farthest_room(base_map)
  #for key in sorted(base_map.keys()):
  #  print(key, base_map[key])
  #print(base_map)
  draw_map(base_map)
  pickle.dump(base_map, open('basepickle.p', 'wb'))
  return base_map

def get_farthest_room(base_map):
  room_dict = {}
  max_distance = 0
  max_room = (0,0)
  for room in base_map:
    distance, path, vtx = dijkstra((0,0), room, base_map)
    room_dict[room] = {'distance':distance, 'path':path}
    if distance > max_distance:
      max_distance = distance
      max_room = room
  #for path in base_map:
  #  print(path)
  print('max distance is', max_distance, 'max room is', max_room)

def find_matching_parenthesis(dirs, i):
  # dirs[i] should be a '(', and so we want to find its partner / closer
  n_pars = 1
  while n_pars > 0:
    i += 1
    if dirs[i] == '(':
      n_pars += 1
    if dirs[i] == ')':
      n_pars -= 1
  return i

def split_out_paths(dirs, i):
  # want to return a list of pointers, e.g. each pointer: [start, end, jumpto]
  grouping_close = find_matching_parenthesis(dirs, i)
  orig = ptr = i+1
  i += 1
  branch_points = []
  while i < grouping_close:
    if dirs[i] == '|':
      branch_points.append(i)
    if dirs[i] == '(':
      close = find_matching_parenthesis(dirs, i)
      i = close
    i += 1
  paths = []
  for point in branch_points:
    paths.append([ptr, point, grouping_close+1])
    ptr = point + 1
  paths.append([ptr, grouping_close, grouping_close+1])
  return paths

def follow_nodes(dirs, branch_queue, base_map, current_room, start = 0):
  # scenarios:
  # 
  #
  if not branch_queue:
    # nothing left to do
    return
  while(branch_queue):
    here, end, jumpto = branch_queue[-1]
    if start > 0:
      here = start
      start = 0
    
    if random.random() > 0.99999:
      draw_map(base_map, current_room)
      print('Depth of queue: {}. Current Index: {}'.format(len(branch_queue), here))
    #if current_room != (0,0):
    #  draw_map(base_map, current_room)
      #print(here, current_room)
      #for b in branch_queue:
      #  print(b, dirs[b[0]:b[1]])
    #  input()

    if here == end:
      # we have reched the end of this sub-branch. 
      branch_queue.pop()
      return follow_nodes(dirs, branch_queue, base_map, current_room, jumpto)
    
    if dirs[here] == '(':
      branches = split_out_paths(dirs, here)
      while len(branches) > 1:
        new_queue = branch_queue[:]
        new_queue.append(branches.pop())
        follow_nodes(dirs, new_queue, base_map, current_room, new_queue[-1][0])
      branch_queue.append(branches.pop())
      return follow_nodes(dirs, branch_queue, base_map, current_room, branch_queue[-1][0])  
    
    next_room = travel(current_room, dirs[here])
    if next_room not in base_map[current_room] and next_room != current_room:
      base_map[current_room].append(next_room)
    if next_room != current_room and current_room not in base_map[next_room]:
      base_map[next_room].append(current_room)
    current_room = next_room
    here += 1
    branch_queue[-1][0] = here


def travel(loc, direction):
  if direction == 'N':
    loc = (loc[0], loc[1] + 1)
  if direction == 'S':
    loc = (loc[0], loc[1] - 1)
  if direction == 'E':
    loc = (loc[0] + 1, loc[1])
  if direction == 'W':
    loc = (loc[0] -1 , loc[1])
  return loc

def dijkstra(p1, p2, graph):
  p1 = tuple(p1)
  p2 = tuple(p2)
  if p1 == p2:
    return 0, [p2], p2
  visited = {}
  notVisited = {}
  for key in graph.keys():
    notVisited[key] = graph[key]

  heap = []
  heapq.heappush(heap, [0, p1, [p1] ])
  first_step = False
  while heap:
    s, thisVtxKey, path = heapq.heappop(heap)
    if thisVtxKey not in visited:
      visited[thisVtxKey] = notVisited.pop(thisVtxKey)
      for vtx in graph[thisVtxKey]:
        if vtx not in visited:
          sum1 = s + 1
          heapq.heappush(heap, [sum1,vtx,path + [vtx]])
          if vtx == p2:
            return sum1, path, vtx
  # well that didn't work, so we return a bunch of 'inf's
  return 10000, [], [] #, [], []float('inf'), [(float('inf'), float('inf'))], (float('inf'), float('inf'))

def draw_map(base_map, loc=None):
  keys = list(base_map.keys())
  minima = np.min(keys, axis=0)
  maxima = np.max(keys, axis=0)
  offsets = -minima
  
  rows = []
  for j in range(maxima[1] - minima[1]+1):
    row = []
    for i in range(maxima[0] - minima[0] + 1):
      x,y = i-offsets[0], j-offsets[1]
      c = get_character((x,y), base_map, loc)
      row.append(c)
    rows.append(''.join(row))

  rows.reverse()
  print('\n----------\n')
  for row in rows:
    print(row)
  print('\n----------\n')

  with open('basemap.txt', 'w') as f:
    for row in rows:
      f.write(row + '\n')

def get_character(point, base_map, loc):
  if loc:
    if point == loc:
      return '0'
  if point not in base_map:
    return ' '
  neighbors = base_map[point]
  
  if point == (0,0):
    return 'X'
  if len(neighbors) == 4:
    return '┼'
  if len(neighbors) == 3:
    if tuple(np.array(point) + np.array((1,0))) not in neighbors:
      return '┤'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors:
      return '├'
    if tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '┬'
    if tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '┴'
  if len(neighbors) == 2:
    if tuple(np.array(point) + np.array((0,-1))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '─'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((1,0))) not in neighbors:
      return '│'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '┌'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '└'
    if tuple(np.array(point) + np.array((1,0))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '┐'
    if tuple(np.array(point) + np.array((1,0))) not in neighbors and tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '┘'
  if len(neighbors) == 1:
    if tuple(np.abs(np.array(point) - np.array(neighbors[0]))) == (1,0):
      return '─'
    else:
      return '│'
      
    

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
