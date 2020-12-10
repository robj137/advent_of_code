import datetime as dt
from collections import Counter
from datetime import datetime as dt
import numpy as np


class Blurb:
    def __init__(self, lines):
        self.lines = [set(x) for x in lines]
        self.total = ''.join(lines)
        self.unique = len(Counter(self.total))
        self.intersection = set.intersection(*self.lines)


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day06.test.txt'
    else:
        in_file = 'inputs/day06.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
 
    blurbs = []
    batch = []
    for line in lines:
        if len(line) < 1:
            if len(batch) > 0:
                blurbs.append(Blurb(batch))
            batch = []
        else:
            batch.append(line.strip())

    if len(batch) > 0:
        blurbs.append(Blurb(batch))

    
    return blurbs

def main():
    data = get_data(is_test=False)
    print(len(data))
    f = [x.unique for x in data]
    g = [x.intersection for x in data]
    print(sum(f))
    print(sum([len(x) for x in g]))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
