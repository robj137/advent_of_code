import datetime as dt
import re

def main():
  p = 'code at row (\d+), column (\d+)'
  with open('inputs/day25.txt') as f:
    l = f.read()
  row, column = [int(x) for x in re.search(p, l).groups()]
  n = get_n_from_row_column(row, column)
  s = 20151125
  for i in range(n-1):
    s = get_next(s)

  print('Part a: the value at row {}, column {} is {}'.format(row, column, s))


def get_n_from_row_column(r, c):
  # first get which diagonal it is
  d = r + c - 1
  n_before = int((d-1)*(d)/2)
  n = n_before + c
  return n

def get_next(n):
  m = n * 252533
  _, remainder = divmod(m, 33554393)
  return remainder

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
