import datetime as dt
import re
import numpy as np
from collections import defaultdict, Counter, deque
import operator

def main():
  
  with open('inputs/day9.txt') as f:
    stream = f.readline().strip()

  stream = take_out_the_trash(stream) # deal with obvious trash (!)
  stream, garbage_count = recycle(stream) # replace <afaslvj lkajf > with 'g'

  score = 0
  rank = 0
  #testing
  #stream = '{{<ab>},{<ab>},{<ab>},{<ab>}}'
  #stream = '{{{},{},{{}}}}'
  for s in stream:
    if s == '{':
      rank += 1
      score += rank
    if s == '}':
      rank -= 1

  
  print('Part a: Score is {}'.format(score))
  print('Part b: Amount recycled: {}'.format(garbage_count))

def recycle(stream):
  garbage_count = 0
  s = deque(stream)
  s.appendleft('_')
  s.rotate(-1)
  while s[0] != '_':
    if s[0] == '<':
      garbage_length = 1
      char = s[0]
      #ok, we are in garbage.
      while char != '>':
        garbage_length += 1
        s.rotate(-1)
        char = s[0]
      # so now garbage_length is the length of garbage
      garbage_count += garbage_length - 2 # do not count <>)
      s.rotate(garbage_length-1)
      while garbage_length:
        s.popleft()
        garbage_length -= 1
      s.appendleft('g')
    s.rotate(-1)
  s.popleft()
  return ''.join(s), garbage_count

def take_out_the_trash(stream):
  s = deque(stream)
  s.appendleft('_') # already checked, it's not in the stream
  s.rotate(-1)
  in_garbage = False
  while s[0] != '_':
    # the goal is to clear out obvious garbage (!)
    # so IF we are not in garbage, then check to see if we enter garbage, and then rotate anyway
    # if we are in garbage, check to see if we are leaving garbage and then rotate if we are
    # check to see if this is ! garbage, and if so, pop it and the next one but don't rotate
    if not in_garbage:
      if s[0] == '<':
        in_garbage = True
      s.rotate(-1)
    else: # we are in garbage
      if  s[0] == '!':
        s.popleft()
        s.popleft()
      else:
        if s[0] == '>':
          in_garbage = False
        s.rotate(-1)
  s.popleft() # getting rid of '_'
  return ''.join(s)

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

