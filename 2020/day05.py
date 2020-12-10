import datetime as dt
from collections import Counter
from datetime import datetime as dt
import numpy as np


def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day05.test.txt'
    else:
        in_file = 'inputs/day05.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    return lines

def parse_seat(code):
    # just use binary. F == 0, B == 1, R == 1, L == 0
    row = code[0:7].replace('F', '0').replace('B', '1')
    row = int(row, 2)
    column = code[7:].replace('R', '1').replace('L', '0')
    column = int(column,2)
    seat_id = 8 * row + column
    return row, column, seat_id

def main():
    data = get_data(is_test=False)

    high_id = 0
    seat_ids = []
    for seat in data:
        _, _, seat_id = parse_seat(seat)
        seat_ids.append(seat_id)
        if seat_id > high_id:
            high_id = seat_id

    print(high_id)
    seat_ids.sort()
    min_id = min(seat_ids)
    max_id = max(seat_ids)
    for i in range(min_id, max_id+1):
        if i not in seat_ids:
            print(i)

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
