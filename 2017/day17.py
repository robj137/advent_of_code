import datetime as dt
import re
import string
from collections import deque, defaultdict

def main():
  puzzle_input = 371
  #puzzle_input = 3

  d = deque([0])
  for i in range(1,2018):
    d.rotate(-1 * puzzle_input)
    d.append(i)

  print('Part a: the value after the last value written is {}'.format(d[0]))

  d = deque([0])
  for i in range(1,50000000):
    d.rotate(-1 * puzzle_input)
    d.append(i)

  zero_index = d.index(0)
  print('Part b: the value after 0 after 5000000 iterations is {}'.format(d[(zero_index+1)%len(d)]))

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))



