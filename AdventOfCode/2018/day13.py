import numpy as np
import datetime as dt
from collections import deque, Counter

signals = {}
signals['^'] = {'step': (0, -1) , '/':'>', '\\':'<', 'l':'<', 's':'^', 'r':'>' }
signals['>'] = {'step': (1, 0) , '/':'^', '\\':'v', 'l':'^', 's':'>', 'r':'v' }
signals['v'] = {'step': (0, 1), '/':'<', '\\':'>', 'l':'>', 's':'v', 'r':'<' }
signals['<'] = {'step': (-1, 0), '/':'v', '\\':'^', 'l':'v', 's':'<', 'r':'^' }


def main():
  with open('inputs/day13.txt') as f:
    tracks = [list(x.strip('\n')) for x in f.readlines()]

  tracks = np.array(tracks)

  cart_list = []
  for cart in ['<', '>', '^', 'v']:
    coords = np.argwhere(tracks==cart)
    for coord in coords:
      c = {}
      c['type'] = cart
      c['x'] = x = coord[1]
      c['y'] = y = coord[0]
      c['next_turn'] = deque(['l', 's', 'r'])
      c['is_crashed'] = False
      cart_list.append(c)
      if cart == '>' or cart == '<':
        tracks[y, x] = '-'
      if cart == 'v' or cart == '^':
        tracks[y, x] = '|'

  ticks = 0
  first_crash = False
  while 1:
    if len(cart_list) == 1:
      break
    ticks += 1
    cart_list = sorted(cart_list, key = lambda cart: 10000*cart['y'] + cart['x'])
    for c in cart_list:
      process_cart(c, tracks)
      if check_for_collisions(cart_list):
        remove_crashes(cart_list)
    removals = []
    for i, c in enumerate(cart_list):
      if c['is_crashed']:
        if not first_crash:
          print('Part a: First crash happens at {},{}'.format(c['x'], c['y']))
          first_crash = True
        removals.append(i)
    removals.sort()
    removals.reverse()
    for i in removals:
      cart_list.pop(i)

  last_cart = cart_list.pop()
  print('Part b: location of last cart, errrr... standing: {},{}'
  .format(last_cart['x'], last_cart['y']))

def remove_crashes(cart_list):
  coords = check_for_collisions(cart_list)
  for cart in cart_list:
    if cart['x'] == coords[0] and cart['y'] == coords[1]:
      cart['is_crashed'] = True

def check_for_collisions(cart_list, p = False):
  cart_coords = [(cart['x'], cart['y']) for cart in cart_list]
  c = Counter(cart_coords)
  if p:
    print(c)
  for key in c:
    if c[key] > 1:
      return key
  return None
  

def process_cart(c, tracks):
  x_offset, y_offset = signals[c['type']]['step']
  c['x'] += x_offset
  c['y'] += y_offset
  road = tracks[c['y'], c['x']]
  if road == '-' or road == '|': # nothing to do
    return
  if road == '/' or road == '\\':
    c['type'] = signals[c['type']][road]
  if road == '+':
    c['type'] = signals[c['type']][c['next_turn'][0]]
    c['next_turn'].rotate(-1)

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
