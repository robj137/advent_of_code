import string
import sys

def get_assignment(r):
    first, last = [int(x) for x in r.split('-')]
    return set([x for x in range(first, last+1)])

if __name__ == '__main__':
    #with open('inputs/day04.test.txt') as f:
    with open('inputs/day04.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    pairs = [x.split(',') for x in lines]
    pairs = [[get_assignment(x[0]), get_assignment(x[1])] for x in pairs]
    print('part 1:', sum([a.intersection(b)in (a,b) for a,b in pairs]))
    print('part 2:', sum([len(a.intersection(b)) > 0 for (a,b) in pairs]))
