import datetime as dt
from scipy.spatial.distance import cdist
import numpy as np
from collections import defaultdict


def part1(coords):
  x_min = coords[:,0].min() - 1
  y_min = coords[:,1].min() - 1
  x_max = coords[:,0].max() + 1
  y_max = coords[:,1].max() + 1
  
  areas = defaultdict(int)
  indices = np.array([(x,y) for x in range(x_min, x_max) for y in range(y_min, y_max)])
  
  for point in indices:
    dists = cdist(coords, [point], 'cityblock')
    min_dist = np.min(dists)
    if np.ravel(dists[dists==min_dist]).shape[0] == 1:
      areas[np.argmin(dists)] += 1
  
  larger_areas = areas.copy()
  x_min = x_min - 1
  y_min = y_min - 1
  x_max = x_max + 1
  y_max = y_max + 1
  points = []
  indices = [(x,y) for x in [x_min-1, x_max+2] for y in range(y_min-1, y_max+2)]
  for point in indices:
    dists = cdist(coords, [point], 'cityblock')
    min_dist = np.min(dists)
    if np.ravel(dists[dists==min_dist]).shape[0] == 1:
      larger_areas[np.argmin(dists)] += 1
      
  finite = {}
  for key in areas:
    if areas[key] == larger_areas[key]:
      finite[key] = areas[key]
  print('Part a: Size of largest (non-infinite) area: {}'.format(max(finite.values())))

def part2(coords):
  x_min = coords[:,0].min() - 2
  y_min = coords[:,1].min() - 2
  x_max = coords[:,0].max() + 2
  y_max = coords[:,1].max() + 2
  indices = np.array([(x,y) for x in range(x_min, x_max) for y in range(y_min, y_max)])
  distances = []
  for point in indices:
    distances.append(np.sum(cdist(coords, [point], 'cityblock')))

  distances = np.array(distances)
  print('Size of the region containing all locations with sum(distance to points) < 10k: {}'
  .format(np.sum(distances<10000)))

def main():
  coords = []
  with open('inputs/day6.txt') as f:
    for line in f:
      x, y = line.strip().split(',')
      coords.append([int(x.strip()), int(y.strip())])
  coords = np.array(coords)
  part1(coords)
  part2(coords)


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
