import datetime as dt
from collections import deque

def main():
  with open('inputs/day1.txt') as f:
    digits = f.read().strip()

  total_next = 0
  total_halfway = 0
  digits = deque(digits)
  halfway = int(len(digits)/2)
  for _ in range(len(digits)):
    if digits[0] == digits[1]:
      total_next += int(digits[0])
    if digits[0] == digits[halfway]:
      total_halfway += int(digits[0])
    digits.rotate()

  print('Part a: Total: {}'.format(total_next))
  print('Part b: Total: {}'.format(total_halfway))

if __name__ == '__main__':                                                                                                                             
  begin = dt.datetime.now()                                                                                                                            
  main()                                                                                                                                               
  diff_time = dt.datetime.now() - begin                                                                                                                
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))                                                            

