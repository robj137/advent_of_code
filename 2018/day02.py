import pandas as pd
import numpy as np
import datetime as dt
from collections import Counter

def compare_serials(s1, s2):
  misses = 0
  for i in range(len(s1)):
    if s1[i] != s2[i]:
      misses += 1
    # if more than one miss, no need to contiue
    if misses > 1:
        return 2
  return misses

def main():
  with open('inputs/day2.txt') as f:
    serials = [x.strip() for x in f.readlines()]

  twos = threes = 0
  for serial in serials:
    c = Counter(serial)
    if 2 in c.values():
      twos += 1
    if 3 in c.values():
      threes += 1

  print('Part a: Checksum = {}'.format(twos * threes))
  
  similar_letters = ''
  for i, s in enumerate(serials):
    for j in range(i, len(serials)):
      if compare_serials(s, serials[j]) == 1:
        s2 = serials[j]
        for k in range(len(s)):
          similar_letters += s[k] if s[k] == s2[k] else ''
  print('Part b: Similar letters: {}'.format(similar_letters))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
