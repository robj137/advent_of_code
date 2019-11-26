import numpy as np
import datetime as dt
from collections import deque

def main():
  data = []
  with open('inputs/day2.txt') as f:
    for line in f:
      data.append([int(x) for x in line.strip().split()])
  data = np.array(data)
  
  checksum = np.sum(np.max(data, axis=1) - np.min(data, axis=1))
  print('Part a: Checksum of the spreadsheet data is {}'.format(checksum))

  sums = 0
  for i in range(data.shape[0]):
    s = deque(data[i,:])
    for j in range(len(s)):
      el = s[0]
      for k in range(1, len(s)):
        if el%s[k] == 0:
          sums += int(el/s[k])
      s.rotate()
  print(sums)

if __name__ == '__main__':                                                                                                                             
  begin = dt.datetime.now()                                                                                                                            
  main()                                                                                                                                               
  diff_time = dt.datetime.now() - begin                                                                                                                
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))                                                            

