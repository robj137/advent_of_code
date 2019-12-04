import pandas as pd
from collections import Counter
import numpy as np
import datetime as dt
from datetime import datetime as dt

def is_valid(i):
    s = str(i)
    if sorted(s) != list(s):
        return False, False
    c = Counter(s)
    return (np.array(list(c.values())) > 1).any(), 2 in c.values()

def main():
    r1 = 231832
    r2 = 767346
    n_a = 0
    n_b = 0
    for i in range(r1, r2+1):
        a, b = is_valid(i)
        if a:
            n_a += 1
        if b:
            n_b += 1

    print('Part 1: Number of sort of valid passwords: {}'.format(n_a))
    print('Part 2: Number of actually valid passwords: {}'.format(n_b))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
