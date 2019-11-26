import re
import numpy as np
from collections import defaultdict
import heapq
from datetime import datetime as dt

def get_look_and_say(s):
    pattern = '(\d)\\1*'
    new_result = ''
    groups = re.finditer(pattern, s)
    for group in groups:
        span = group.span()
        span = span[1] - span[0]
        digit = group[0][0]
        new_result += str(span) + digit
    return new_result

def main():
       
    puzzle_input = '1113222113'
    s = puzzle_input
    for i in range(40):
        s = get_look_and_say(s)

    part_1_answer = len(s)
    print('Part 1: Length of new result after L&S is {}'.format(part_1_answer))

    for i in range(10):
        s = get_look_and_say(s)

    part_2_answer = len(s)
    print('Part 2: Length of new result after L&S is {}'.format(part_2_answer))

if __name__ == '__main__':
  begin = dt.now()
  main()
  diff_time = dt.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
