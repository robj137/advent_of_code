import datetime as dt
import numpy as np

def get_ring(number):
  r = int(number**0.5-0.0001)
  if r%2 == 0:
    r -= 1
  return int((r+1)/2)

def get_start_of_ring(ring):
  r = 2* ring - 1
  if r%2 == 0:
    r += 1
  start = r*r+1
  start_x, start_y = ring, -(ring-1)
  return start, start_x, start_y

def get_grid_mapping(number):
  ring = get_ring(number)
  value, x, y = get_start_of_ring(ring)
  if value == number:
    return x, y
  for i in range(2*ring-1):
    y += 1
    value += 1
    if value == number:
      return x, y
  for i in range(2*ring):
    x -= 1
    value += 1
    if value == number:
      return x, y
  for i in range(2*ring):
    y -= 1
    value += 1
    if value == number:
      return x, y
  for i in range(2*ring):
    x += 1
    value += 1
    if value == number:
      return x, y

def main():
  puzzle_input = 347991
  x, y = get_grid_mapping(puzzle_input)
  manhattan_distance = np.abs(x) + np.abs(y)
  print('Part a: distance from {} to the origin is {}'.format(puzzle_input, manhattan_distance))

  value_dict = {}
  value_dict[(0,0)] = 1

  for k in range(2,100):
    x, y = get_grid_mapping(k)
    square_total = 0
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        if (i,j) in value_dict:
          square_total += value_dict[(i,j)]
    value_dict[(x,y)] = square_total
    if square_total > puzzle_input:
      break
  print('Part b: first value written larger than puzzle input: {}'.format(square_total))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

