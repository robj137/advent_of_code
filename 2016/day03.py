import datetime as dt
import numpy as np

def main():
  with open('inputs/day3.txt') as f:
    triangles = [[y for y in map(int, x.strip().split())] for x in f.readlines()]# for x in y.strip().split()]
  
  triangles = np.array(triangles)
  possibles = []
  for t in triangles:
    t_s = sorted(t, reverse=True)
    if t_s[0] < sum(t_s[1:]):
      possibles.append(t)

  print(len(possibles))

  t2 = triangles.ravel(order='F').reshape(triangles.shape)
  possibles2 = []
  for t in t2:
    t_s = sorted(t, reverse=True)
    if t_s[0] < sum(t_s[1:]):
      possibles2.append(t)
  print(len(possibles2))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
