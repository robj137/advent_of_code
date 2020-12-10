import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime as dt

def get_data():
    in_file = 'inputs/day01.txt'
    with open(in_file) as f:
        lines = f.readlines()
    return [int(x.strip()) for x in lines]


def main():
    data = np.array(get_data())
    desired_sum = 2020
    a = b = None
    N = len(data)
    for i in range(N):
        a = data[i]
        for j in range(i, N):
            b = data[j]
            if a + b == desired_sum:
                print(a, b, a*b)

def main2():
    data = np.array(get_data())
    desired_sum = 2020
    a = b = c = None
    N = len(data)
    for i in range(N):
        a = data[i]
        for j in range(i, N):
            b = data[j]
            for k in range(j, N):
                c = data[k]
                if a + b + c == desired_sum:
                    print(a, b, c,  a*b*c)
                    return

if __name__ == '__main__':
    begin = dt.now()
    main()
    main2()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
