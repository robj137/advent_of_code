import operator
import numpy as np
import datetime as dt
import re
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd

def get_map():
  nanobot_map = {}
  pattern = 'pos=<(.*),(.*),(.*)>, r=(\d+)'
  with open('inputs/day23.txt') as f:
    for line in f:
      x,y,z,r = re.search(pattern, line.strip()).groups()
      nanobot_map[(int(x),int(y),int(z))] = int(r)
  return nanobot_map

def main():
  nanobot_map = get_map()
  strongest_signal = max(nanobot_map.items(), key=operator.itemgetter(1))[0]
  in_range = 0
  for signal in nanobot_map:
    dist = get_distance(signal, strongest_signal)
    if dist <= nanobot_map[strongest_signal]:
      #print(signal, 'is in range with distance', dist )
      in_range += 1
    #else:
    #  print(signal, 'is not in range with distance', dist)
  print('Part a: Number of nanobots in range of strongest signal: {}'.format(in_range))


  coords = []
  for p1 in nanobot_map.keys():
    in_range = 0
    for p2 in nanobot_map.keys():
      if get_distance(p1, p2) <= nanobot_map[p2]:
        in_range += 1
    coords.append([p1[0],p1[1],p1[2], nanobot_map[p1], in_range])
  z = np.array(coords)
  df = pd.DataFrame(coords, columns=['x', 'y', 'z', 'r', 'in_range'])
  df['point'] = list(zip(df['x'], df['y'], df['z']))
 
  max_value = 0
  best_location = (0,0,0)
  for p in df['point'].items():
    print('On bot #', p)
    value, location = anneal(p[1], nanobot_map, 'crawl')
    if value >= max_value:
      print('new max value:', value, 'at location', location)
      #print('found a match for {}'.format(p[1]))
      max_value = value
      best_location = location

  print(max_value, best_location)
  #fig, ax = plt.subplots(1, 3)
  #df.plot.scatter(x='x', y='y', ax=ax[0])
  #df.plot.scatter(x='x', y='z', ax=ax[1])
  #df.plot.scatter(x='y', y='z', ax=ax[2])
  #plt.show()
  #print(df.describe())
  #return df

  

# 58350000,47499992,52795500 wasn't right (877)
# as in 158645492 is too low (and so is 877)
# 900, 158870979 too low
# 903, 160646346 too low
# 905, 160646361 
def anneal(p1, nanobot_map, method = 'random', optimize=False):
  max_value = get_n_within_range(p1, nanobot_map)
  best_location = p1
  next_step = np.array([0,0,0])
  #print('Initial value of {} at {}'.format(max_value, p1))
  if method == 'grid':
    for i in range(-20, 20):
      for j in range(-20, 20):
        for k in range(-20, 20):
          step = next_step.copy()
          step = (i,j,k)
          p_next = tuple(np.array(best_location) + step)
          trial = get_n_within_range(p_next, nanobot_map)
          if trial > max_value:
            #print('new best of {} at {}'.format(trial, p_next))
            max_value = trial
  if method == 'crawl':
    while(1):
      previous_max_value = max_value
      for p in range(9, -1, -1):
        for j in range(-9,10):
          for i in range(3):
            step = next_step.copy()
            step[i] = j * (10**p)
            p_next = tuple(np.array(best_location) + step)
            trial = get_n_within_range(p_next, nanobot_map)
            if trial > max_value:
              #print('new best of {} at {}'.format(trial, p_next))
              max_value = trial
              best_location = p_next
          for i in range(3):
            step = next_step.copy()
            step[0] = step[1] = step[2] = j * (10**p)
            step[i] = 0
            p_next = tuple(np.array(best_location) + step)
            trial = get_n_within_range(p_next, nanobot_map)
            if trial > max_value:
              #print('new best of {} at {}'.format(trial, p_next))
              max_value = trial
              best_location = p_next
      if max_value == previous_max_value:
        break
  if method == 'random':
    steps = 10000
    max_power_step = 10
    while steps and max_power_step:
      ax = np.random.randint(10)
      p = 10**(np.random.randint(max_power_step))
      if ax < 3:
        next_step[ax] = int(np.random.random() * p)
      else:
        next_step[0] = int(np.random.random() * p)
        next_step[1] = int(np.random.random() * p)
        next_step[2] = int(np.random.random() * p)
      p_next = tuple(np.array(best_location) + next_step)
      trial = get_n_within_range(p_next, nanobot_map)
      if trial > max_value:
        #print('new best of {} at {}'.format(trial, p_next))
        max_value = trial
        best_location = p_next
        steps = 1000
      #if trial == max_value and get_distance((0,0,0), p_next) < get_distance((0,0,0), best_location):
      #  best_location = p_next
      steps -= 1
      if not steps:
        steps = 1000
        max_power_step -= 1
        print('stepping down')
      
      next_step[0] = next_step[1] = next_step[2] = 0
  
  if optimize:
    # now to find the coordinate nearest 0,0,0

    previous_best_location = (0,0,0)
    while(previous_best_location != best_location):
      previous_best_location = best_location
      for p in range(9, -1, -1):
        for i in range(3):
          for j in range(-9,10):
            step = next_step.copy()
            step[i] = j * (10**p)
            p_next = tuple(np.array(best_location) + step)
            trial = get_n_within_range(p_next, nanobot_map)
            if trial >= max_value and get_distance((0,0,0), p_next) < get_distance((0,0,0), best_location):
              print('new best of {} at {}'.format(trial, p_next))
              max_value = trial
              best_location = p_next
  
    return max_value, best_location, get_distance((0,0,0), best_location)

  return max_value, best_location

def get_n_within_range(p1, nanobot_map):
  n = 0
  for c in nanobot_map.keys():
    if get_distance(p1,c) <= nanobot_map[c]:
      n += 1
  return n

def get_distance(p1, p2):
  x1,y1,z1 = p1
  x2,y2,z2 = p2
  d = abs(x1-x2) + abs(y1-y2) + abs(z1-z2)
  return d

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
