import sys
import numpy as np
import datetime as dt
from collections import defaultdict

def translate_to_array(b):
  # b is like ...#/.####
  raw_rows = b.split('/')
  s = len(raw_rows)
  rows = []
  for r in raw_rows:
    row = []
    for el in r:
      row.append(1 if el == '#' else 0)
    rows.append(row)
  return np.array(rows)

def parse_line(line, d):
  pre = translate_to_array(line.split(' => ')[0])
  post = translate_to_array(line.split(' => ')[1])
  for k in range(4):
    pre = np.rot90(pre, k)
    d[str(pre)] = post
    d[str(np.flip(pre, axis=1))] = post

def propagate_art(d, picture):
  exploded = blockshaped(picture)
  l = []
  for i in range(exploded.shape[0]):
    l.append(d[str(exploded[i])])

  l = np.array(l)
  return unblockshaped(l)


def unblockshaped(arr):
  """
  Return an array of shape (h, w) where
  h * w = arr.size

  If arr is of shape (n, nrows, ncols), n sublocks of shape (nrows, ncols),
  then the returned array preserves the "physical" layout of the sublocks.
  """
  n, nrows, ncols = arr.shape
  w = int(n**0.5*nrows)
  return (arr.reshape(w//nrows, -1, nrows, ncols)
             .swapaxes(1,2)
             .reshape(w, w))

def blockshaped(arr):
  """
  Return an array of shape (n, nrows, ncols) where
  n * nrows * ncols = arr.size

  If arr is a 2D array, the returned array should look like n subblocks with
  each subblock preserving the "physical" layout of arr.
  """
  shape = arr.shape
  if shape[0] != shape[1]:
    sys.exit('really? comeon ')
  w = arr.shape[0]
  if w%2 == 0:
    nrows = 2
    n_blocks_side = int(w/2)
  else:
    nrows = 3
    n_blocks_side = int(w/3)
  ncols = nrows
  return (arr.reshape(n_blocks_side, nrows, -1, ncols)
        .swapaxes(1,2)
        .reshape(-1, nrows, ncols))


def populate_dict():
  with open('inputs/day21.txt') as f:
    lines = [x.strip() for x in f.readlines()]
  d = defaultdict(str)
  for line in lines:
    parse_line(line, d)
  return d

def main():
  d = populate_dict()
  art = np.array([[0,1,0],[0,0,1],[1,1,1]])
  print(art)
  print('Found {} lights on at the beginning'.format(np.sum(art)))
  for i in range(18):
    art = propagate_art(d, art)
    print(art)
    print('Found {} lights on after {} iterations'.format(np.sum(art), i+1))
    
    

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

