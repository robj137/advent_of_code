import hashlib
import string
from collections import defaultdict, deque

def is_nice(s):
  if 'ab' in s or 'cd' in s or 'pq' in s or 'xy' in s:
    return False
  double_valid = False
  for x in string.ascii_lowercase:
    if (x+x) in s:
      double_valid = True
  if not double_valid:
      return False
  d = defaultdict(int)
  for letter in s:
    d[letter] += 1
  if d['a'] + d['e'] + d['i'] + d['o'] + d['u'] <3:
    return False
  return True

def is_nice_2(s):
  is_repeat = False
  is_valid_pair = False
  for i in range(len(s)-2):
    if s[i] == s[i+2]:
      is_repeat = True
  for i in range(len(s)-2):
    if s[i:i+2] in s[0:i] or s[i:i+2] in s[i+2:]:
      is_valid_pair = True
  return is_repeat and is_valid_pair

def main():
  lines = []
  with open('inputs/day5.txt') as f:
    for line in f:
      lines.append(line.strip())

  nice_strings = []
  nice_strings2 = []
  for line in lines:
    #if is_nice(line):
    #  nice_strings.append(line)
    if is_nice_2(line):
      nice_strings2.append(line)
  nice_strings2 = list(set(nice_strings2))
  print(len(nice_strings2))
  for i in nice_strings2:
    print(i)
  #print(len(nice_strings))
if __name__ == '__main__':
  main()

