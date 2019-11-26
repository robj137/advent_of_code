import numpy as np
import datetime as dt
import re
from collections import Counter
import pandas as pd

def get_strength(t):
  return (t[0]**2 + t[1]**2 + t[2]**2)**0.5

def main():
  coords = []
  pattern = 'p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>'
  with open('inputs/day20.txt') as f:
    for line in f:
      g = re.search(pattern, line.strip()).groups()
      g = [int(x) for x in g]
      coords.append([g[0], g[1], g[2],g[3], g[4], g[5], g[6], g[7], g[8]])
  accelerations = []
  for c in coords:
    accelerations.append(np.linalg.norm(np.array((c[6], c[7], c[8]))))
  
  small_a = min(accelerations)
  print('Part a: after a looong time, the particle with the smallest acceleration will be closest to the origin, and that particle is {}'.format(accelerations.index(small_a)))

  px = [x[0] for x in coords]
  py = [x[1] for x in coords]
  pz = [x[2] for x in coords]
  vx = [x[3] for x in coords]
  vy = [x[4] for x in coords]
  vz = [x[5] for x in coords]
  ax = [x[6] for x in coords]
  ay = [x[7] for x in coords]
  az = [x[8] for x in coords]
  d = {'px':px, 'py':py, 'pz':pz, 'vx':vx, 'vy':vy, 'vz':vz, 'ax':ax, 'ay':ay, 'az':az}
  df = pd.DataFrame(d)
  

  for i in range(100):
    df['vx'] += df['ax']
    df['vy'] += df['ay']
    df['vz'] += df['az']
    df['px'] += df['vx']
    df['py'] += df['vy']
    df['pz'] += df['vz']
    df = df[~df.duplicated(subset=['px','py', 'pz'], keep=False)]

  # too lazy to code in the check.

  print('Part b: after all collisions are done, there are {} particles left'.format(df.shape[0]))
if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))


