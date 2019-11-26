import datetime as dt
from collections import defaultdict, deque
import numpy as np

def main():
  scanner_dict = defaultdict(dict)
  lines = []
  with open('inputs/day13.txt') as f:
    for line in f:
      depth = int(line.split(':')[0])
      r = int(line.split(':')[1])
      scanner_dict[depth] = {'depth':depth, 
                             'range': r,
                             'is_on': deque([x for x in range(2*(r-1))]),
                             'n_rotations': 0,
                             'severity':depth*r}

  initial_severity = get_severity(scanner_dict)
  print('Part a: Leaving at time 0 results in a severity of {}'.format(initial_severity))

  clean_delay = 0
  # delay is actually 3921270 for me. ugh, need to make this faster
  for delay in range(3000000,4000000):
    if delay%10000 == 0:
      print(delay/1e6)
    severity = get_severity(scanner_dict, delay)
    if severity == 0:
      clean_delay = delay
      break
  if clean_delay > 0:
    print('Part b: Leaving after {} picoseconds results in a clean trip'.format(delay))

def get_severity(scanner_dict, delay = 0):
  for key in scanner_dict.keys():
    scanner_dict[key]['is_on'].rotate(-scanner_dict[key]['n_rotations'])
    scanner_dict[key]['n_rotations'] = 0
  [update_scanner(x, scanner_dict, delay) for x in scanner_dict.keys()]
  total_severity = 0
  layer = -1
  picoseconds = 0
  while picoseconds < max(scanner_dict.keys()) + 4:
    #if layer in scanner_dict:
    #  print(layer, scanner_dict[layer)
    layer += 1
    if layer in scanner_dict.keys():
      if scanner_dict[layer]['is_on'][0] == 0:
        if delay > 0:
          return 1
          return layer if layer > 0 else -1
        total_severity += scanner_dict[layer]['severity']
    [update_scanner(x, scanner_dict) for x in scanner_dict.keys()]
    picoseconds += 1

  return total_severity

def update_scanner(depth, scanner_dict, n_times=1):
  scanner = scanner_dict[depth]
  scanner['is_on'].rotate(n_times)
  scanner['n_rotations'] += n_times

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

