import numpy as np
import datetime as dt
from collections import defaultdict

def main():
  with open("inputs/day20.txt") as f:
    turns = f.read().strip("\n")

  dir_dict = {}
  dir_dict["E"] = np.array((1, 0))
  dir_dict["W"] = np.array((-1, 0))
  dir_dict["S"] = np.array((0, 1))
  dir_dict["N"] = np.array((0, -1))

  room_dict = defaultdict(set)
  room_lengths = defaultdict(int)
  branches = []
  p_previous = p = (0, 0)
  
  for turn in turns[1:-1]:
    # dealing with the lovely branches. When we come to a (, we push that room location onto a list
    # when we hit the branch divider |, it means we've processed a branch, and so we return our
    # room pointer to the beginning of the branch
    if turn == "(":
      branches.append(p)
    elif turn == "|":
      p = branches[-1]
    elif turn == ")":
      #p = 
      branches.pop()
    else:
      p = tuple(np.array(p) + dir_dict[turn])
      room_dict[p].add(p_previous)
      room_dict[p_previous].add(p)
      # previously I had filled the room_dict, and THEN looped over the rooms to find the farthest
      # this is soooo much faster than traversing the room map after it's created (changed after 
      # looking at the reddit megathread. But 5 minutes -> 500 ms is a bit of an increase in
      # efficiency  (and most of that is drawing the map ) :)
      if room_lengths[p] != 0:
        room_lengths[p] = min(room_lengths[p], room_lengths[p_previous]+1)
      else:
        room_lengths[p] = room_lengths[p_previous] + 1
    p_previous = p


  draw_map(room_dict)
  print('Part a: Shortest path to farthest room is {} doors'.format(max(room_lengths.values())))
  print('Part b: There are {} rooms that have a shortest path of at least 1000 doors'
        .format(len([x for x in room_lengths.values() if x >= 1000])))

  print('By the way, there are {} rooms total'.format(len(room_lengths)))
  
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

  #rows.reverse()
  for row in rows:
    print(row)

  with open('basemap.txt', 'w') as f:
    for row in rows:
      f.write(row + '\n')

def get_character(point, base_map, loc):
  if loc:
    if point == loc:
      return '0'
  if point not in base_map:
    return ' '
  neighbors = list(base_map[point])
  
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
      return '┴'
    if tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '┬'
  if len(neighbors) == 2:
    if tuple(np.array(point) + np.array((0,-1))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '─'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((1,0))) not in neighbors:
      return '│'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '└'
    if tuple(np.array(point) + np.array((-1,0))) not in neighbors and tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '┌'
    if tuple(np.array(point) + np.array((1,0))) not in neighbors and tuple(np.array(point) + np.array((0,1))) not in neighbors:
      return '┘'
    if tuple(np.array(point) + np.array((1,0))) not in neighbors and tuple(np.array(point) + np.array((0,-1))) not in neighbors:
      return '┐'
  if len(neighbors) == 1:
    if tuple(np.array(point) - np.array(neighbors[0])) == (1,0):
      return '─'
    if tuple(np.array(point) - np.array(neighbors[0])) == (-1,0):
      return '─'
    if tuple(np.array(point) - np.array(neighbors[0])) == (0,1):
      return '╵'
    if tuple(np.array(point) - np.array(neighbors[0])) == (0,-1):
      return '╷'

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
