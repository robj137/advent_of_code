import pandas as pd
import numpy as np
import datetime as dt

def main():
  df = pd.read_csv('inputs/day3.txt', header=None, delimiter=' ')  
  df.index = df[0].apply(lambda x: int(x[1:]))
  df['x_1'] = df[2].apply(lambda x: int(x.split(',')[0]))
  df['y_1'] = df[2].apply(lambda x: int(x.split(',')[1].strip(':')))
  df['x_size'] = df[3].apply(lambda x: int(x.split('x')[0]))
  df['y_size'] = df[3].apply(lambda x: int(x.split('x')[1]))
  df = df.drop([0,1,2,3], axis=1) # should use regex instead of split magic
  df['x_2'] = df['x_1'] + df['x_size']
  df['y_2'] = df['y_1'] + df['y_size']

  canvas = np.zeros([1000,1000])
  for n, row in df.iterrows():
    x1 = row['x_1']
    x2 = row['x_2']
    y1 = row['y_1']
    y2 = row['y_2']
    canvas[x1:x2,y1:y2] += 1

  print('Part a: square inches of fabric with > 1 claim: {}'.format((canvas >= 2).sum()))
  print('square inches of fabric with only 1 claim: {}'.format((canvas == 1).sum()))
  
  for n, row in df.iterrows():
    x1 = row['x_1']
    x2 = x1 + row['x_size']
    y1 = row['y_1']
    y2 = y1 + row['y_size']
    if np.array_equal(np.ones([row['x_size'], row['y_size']]), canvas[x1:x2,y1:y2]):
      print('Part b: row id for only claim that doesn\'t overlap: {}'.format(n))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
