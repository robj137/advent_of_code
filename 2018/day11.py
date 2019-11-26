import numpy as np
import datetime as dt
from multiprocessing import Process, Queue

def get_power(p, serial):
  rackId = p[:,0] + 10
  power = rackId * p[:,1] + serial
  power *= rackId
  power = ((power/100)%10).astype(int)
  power -= 5
  return power

def get_subgrid(p, grid_size, power_grid):
  return power_grid[p[:,0]:p[:,0]+grid_size, p[:,1]:p[:,1]+grid_size]


def crunch_grid(N, power_grid, q):
  max_power = x_max = y_max = gs_max = 0
  for grid_size in N:
    z = [(x,y) for x in range(300 - grid_size + 1) for y in range(300 - grid_size + 1)]
    for x, y in z:
      power = np.sum(power_grid[x:x+grid_size,y:y+grid_size])
      if power > max_power:
        x_max = x+1
        y_max = y+1
        max_power = power
        gs_max = grid_size
    if grid_size == 3:
      print('For size grid = 3, max_power = {}, x_max = {}, y_max = {}'.format(max_power, x_max, y_max))
  q.put((max_power, x_max, y_max, gs_max))

def main():
  # so part a takes less than a second
  # and part b takes less than 3 minutes :P
  begin = dt.datetime.now()
  serial = 7511
  grid_points = np.array([(x,y) for x in range(1,301) for y in range(1,301)])
  power_grid = np.reshape(get_power(grid_points, serial), (300,300))


  N = np.array([x for x in range(3,300)])
  n_procs = 2
  ranges = []
  for i in range(n_procs):
    ranges.append(N[N%n_procs == i])
  
  q = Queue()
  
  procs = [Process(target=crunch_grid, args=(r, power_grid, q)) for r in ranges]
  results = []
  
  [p.start() for p in procs]
  
  [results.append(q.get(True)) for x in procs]

  [p.join() for p in procs]
  results= np.array(results)
  cols = results.transpose()
  ndx = np.argmax(cols[0,:])
  best = results[ndx]
  print('Found max power of {} at grid size {}, x = {}, y = {}'
  .format(best[0], best[3], best[1], best[2]))
    
  d = dt.datetime.now() - begin
  print('And the whole thing took {:.3f} seconds'.format(d.seconds + 1e-6*d.microseconds))

if __name__ == '__main__':
  main()
