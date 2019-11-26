import string
from datetime import datetime as dt
import json

def delve(o, ignore_red=False):
    s = 0
    if type(o) == int:
        return int(o)
    if type(o) == str:
        return s
    if type(o) == list:
        for element in o:
            s += delve(element, ignore_red)
        return s
    # else it's a dict 
    if not ignore_red: # and 'red' not in o.values():
        for key in o.keys():
            s += delve(o[key], ignore_red)
    if ignore_red and 'red' not in o.values():
        for key in o.keys():
            s += delve(o[key], ignore_red)

    return s

def main():
    
    puzzle_input = json.loads(open('inputs/day12.txt', 'r').read())

    print(delve(puzzle_input, True))

    print('Part 1: Sum of all numbers is {}'.format(delve(puzzle_input, False)))
    print('Part 2: Sum of all numbers (ignoring red) is {}'.format(delve(puzzle_input, True)))

if __name__ == '__main__':
  begin = dt.now()
  main()
  diff_time = dt.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
