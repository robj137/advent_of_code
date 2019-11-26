import datetime as dt
from collections import Counter
import numpy as np

def main():
  steps = []
  with open('inputs/day11.txt') as f:
    steps = [x for x in f.read().strip().split(',')]

  pi = 4*np.arctan(1)
  directions = ['ne', 'n', 'nw', 'sw', 's', 'se']
  angles = [pi/6 + i * pi/3 for i, _ in enumerate(directions)]
  bundled = zip(directions, angles)
  distance_dict = {}
  for direction, angle in bundled:
    distance_dict[direction] = np.array([np.cos(angle), np.sin(angle)])
  #c = Counter(steps)
  #print(c)
  print(distance_dict)
  location = np.array([0.0,0.0])
  steps_away = []
  for step in steps:
    location += distance_dict[step]
    steps_away.append(get_required_steps(location)[2])
  
  x_steps, y_steps, total_steps = get_required_steps(location)
  print('Part a: the number of x {} and y {} steps needed sums to {}'
        .format(int(x_steps), int(y_steps), int(x_steps) + int(y_steps)))

  print('Part b: the max number of steps away was {}'.format(max(steps_away)))

def get_required_steps(location):
  #so traveling n/s is easy. But how many e/w steps does it take to get to the x=0 line?
  # one step nw/ne/sw/se is cos(pi/6) (about 0.866) in x and sin(pi/6) in y
  pi = 4*np.arctan(1)
  
  x_steps = np.abs(np.round((location[0] / np.cos(pi/6))))

  y_distance_covered = 0.5 * x_steps
  y_steps = np.abs(location[1]) - np.abs(y_distance_covered)
  
  return int(x_steps), int(y_steps), int(x_steps + y_steps)


if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

