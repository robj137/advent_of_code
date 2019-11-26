import datetime as dt
import numpy as np
from collections import Counter

def main():
  with open('inputs/day6.test.txt') as f:
    codes = [x.strip() for x in f.readlines()]
  
  code1 = ''
  code2 = ''
  codes = np.array([list(x) for x in codes])
  codes = codes.T
  for line in codes:
    code1 += Counter(line).most_common()[0][0]
    code2 += Counter(line).most_common()[-1][0]
  print('Part a: the crapply code is {}'.format(code1))
  print('Part b: the actual code is {}'.format(code2))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
