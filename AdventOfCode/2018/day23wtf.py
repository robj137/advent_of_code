
import sys,re
from queue import PriorityQueue
import datetime as dt

def main():
  with open('inputs/day23.txt') as f:
    lines = f.readlines()
  bots = [map(int, re.findall("-?\d+", line)) for line in lines]
  q = PriorityQueue()
  for x,y,z,r in bots:
    d = abs(x) + abs(y) + abs(z)
    q.put((max(0, d - r),0.001, (x,y,z,r)))
    q.put((d + r + 1,-2, (x,y,z,r)))
  count = 0
  maxCount = 0
  result = 0
  coord = None
  print(q.qsize())
  while not q.empty():
    dist,e,woof = q.get()
    count += e
    print(dist, e, woof)
    if count > maxCount:
      coord = woof
      result = dist
      maxCount = count
  print(result)
  print(coord)

if __name__ == '__main__':
 begin = dt.datetime.now()
 main()
 diff_time = dt.datetime.now() - begin
 print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
