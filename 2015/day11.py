import re
import numpy as np
import string
from datetime import datetime as dt

l = string.ascii_lowercase
triplets = [l[i:i+3] for i in range(len(l)-2)] 

def check_password(s):
    if 'i' in s or 'o' in s or 'l' in s:
        return False
    pattern = '(\w)\\1+'
    if len([x for x in re.finditer(pattern, s)]) < 2:
        return False
    for t in triplets:
        if t in s:
            return True
    return False

def increment_password(s):
    s = list(s)
    i = len(s) - 1
    # 122 -> 97
    # 104 -> 106
    while i > -1:
        if ord(s[i] ) == 122:
            s[i] = 'a'
            i -= 1
        else:
            s[i] = chr(ord(s[i]) + 1)
            break
    return ''.join(s)

def main():
    
    puzzle_input = 'cqjxjnds'
    #puzzle_input = 'abcdefgh'

    l = puzzle_input
    while not check_password(l):
        #print(l)
        l = increment_password(l)

    part_1_answer = l
    print('Part 1: Santa\'s next password is {}'.format(part_1_answer))

    l = increment_password(l)
    while not check_password(l):
        l = increment_password(l)
    
    part_2_answer = l
    print('Part 2: Santa\'s next password is {}'.format(part_2_answer))


if __name__ == '__main__':
  begin = dt.now()
  main()
  diff_time = dt.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
