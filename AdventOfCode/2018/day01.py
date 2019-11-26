import datetime as dt
from collections import deque

def main():
    in_file = open('inputs/day1.txt')
    shifts = []
    with open('inputs/day1.txt') as f:
        shifts = deque([int(x.strip()) for x in f.readlines()])
    print('Part A: The frequency shifts end at {}'.format(sum(shifts)))
    
    current_frequency = 0
    dupes = {current_frequency:0}
    dupe = False
    shifts.rotate()

    while(1):
        shifts.rotate(-1)
        current_frequency += shifts[0]
        if current_frequency not in dupes:
            dupes[current_frequency] = 0
        else:
            print('Part B: Found duplicated frequency at {}'
                    .format(current_frequency))
            return

if __name__ == '__main__':
    begin = dt.datetime.now()
    main()
    diff_time = dt.datetime.now() - begin
    print('That took {:.6f} seconds'.format(
            diff_time.seconds 
            + 1e-6*diff_time.microseconds
            )
    )
