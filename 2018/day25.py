import pandas as pd
import numpy as np
import datetime as dt


def get_distance(p1, p2):
  return np.sum(np.abs(p1-p2))

def get_coords():
  with open('inputs/day25.txt') as f:
    lines = f.readlines()
  coords = []
  for line in lines:
    x,y,z,t = line.split(',')
    coords.append(np.array([int(x), int(y), int(z), int(t)]))
  return coords

def main():
  coords = get_coords()

  constellation_dict = {}
  for c1 in coords:
    constellation_dict[tuple(c1)] = []
    for c2 in coords:
      d = get_distance(c1, c2)
      if d > 0 and d <= 3:
        constellation_dict[tuple(c1)].append(tuple(c2))


  constellations = []
  current_constellation = None
  previous_current_constellation_size = 0
  while constellation_dict:
    if not current_constellation:
      current_constellation_seed = list(constellation_dict.keys())[0]
      current_constellation = [current_constellation_seed]
    for star in current_constellation:
      for neighbor in constellation_dict[star]:
        if neighbor not in current_constellation:
          current_constellation.append(neighbor)
    if current_constellation:
      if len(current_constellation) == previous_current_constellation_size:
        # looping is done, current_constellation is full, so cleanup.
        constellations.append(current_constellation)
        keys = sorted(constellation_dict.keys())
        for key in keys:
          if key in current_constellation:
            del constellation_dict[key]
        current_constellation = None
        previous_current_constellation_size = 0
      else:
        previous_current_constellation_size = len(current_constellation)

  print(len(constellations), constellations)

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
