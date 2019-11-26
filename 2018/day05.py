import string
from collections import deque
import datetime as dt
import operator

def is_same_letter_opposite_case(c1,c2):
  return abs(ord(c1) - ord(c2)) == 32

def compress(a_string):
  a_string = deque(a_string)
  a_string.append('-') # it's circular now, but dont' want to risk first and last being conjugates
  n_rotations = 0
  while n_rotations < len(a_string):
    if is_same_letter_opposite_case(a_string[0], a_string[1]):
      a_string.popleft()
      a_string.popleft()
      n_rotations = 0 # reset
    else:
      a_string.rotate()
      n_rotations += 1
  
  return len(a_string) - 1 # remember to subtract one b.c. we added a '-'

def main():
  types = ''
  with open('inputs/day5.txt') as f:
    types = f.read().strip()
  types_less_one = types
  
  print('Part a: Units remaining after polymer contraction: {}'.format(compress(types)))

  removal_dict = {}
  for letter in string.ascii_lowercase:
    removal_dict[letter] = compress(types.replace(letter,'').replace(letter.upper(),''))
  
  print('Part b: Minimum possible polymer length: {}'.format(min(removal_dict.values())))


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
