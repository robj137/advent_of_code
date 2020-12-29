import array
import datetime as dt
from collections import deque
from datetime import datetime as dt
import numpy as np


def get_data(is_test=True):
    if is_test:
        val = '389125467'
    else:
        val ='792845136'
    return [int(x) for x in val]
    #return deque([int(x) for x in val])

def run_alt(cup_labels, n_cups, n_rounds):
    # version that uses a list to keep track of a cup's next position
    # e.g. lookup[1] gives the cup following 1.
    # we'll use lookup[0] to keep track of the curent cup
    lookup = [-1] * (n_cups + 1)
    initial_cups = [int(x) for x in cup_labels]
    # first initialize the cup labels
    first_one = initial_cups[0]
    current_cup = first_one
    for i in range(1, len(cup_labels)):
        lookup[current_cup] = initial_cups[i]
        current_cup = lookup[current_cup]
    
    # fill out the rest of the list if n_cups > len(cup_labels)
    for i in range(len(initial_cups) + 1, n_cups + 1):
        lookup[current_cup] = i
        current_cup = i
    lookup[current_cup] = first_one

    current_cup = first_one
    aside = [0,0,0]
    for i in range(n_rounds):
        aside[0] = lookup[current_cup]
        aside[1] = lookup[aside[0]]
        aside[2] = lookup[aside[1]]
        
        destination_cup = (current_cup - 2)%n_cups + 1
        while destination_cup in aside:
            destination_cup = (destination_cup - 2)%n_cups + 1
        lookup[current_cup] = lookup[aside[2]]
        lookup[aside[2]] = lookup[destination_cup]
        lookup[destination_cup] = aside[0]
        current_cup = lookup[current_cup]

    return lookup

def run_round(d):
    # original way for part 1, uses a deque.
    # too slow for part 2
    current = d[0]
    max_d = max(d)
    d.rotate(-1)
    extra = []
    for i in range(3):
        extra.append(d.popleft())
    
    destination = current - 1
    inc = 0
    while destination not in d:
        inc += 1
        destination -= 1
        if destination  <1:
            destination = max_d
    while d[-1] != destination:
        d.rotate()
    d.extend(extra)
    
    while d[0] != current:
        d.rotate(-1)

    d.rotate(-1)

if __name__ == '__main__':
    begin = dt.now()
    is_test = False

    circle = deque(get_data(is_test))
    for i in range(100):
        run_round(circle)
    while circle[0] != 1:
        circle.rotate()
    circle.popleft()
    part_1_answer = ''.join([str(x) for x in circle])
    diff_time = dt.now() - begin
    print('Part 1: {}'.format(part_1_answer))
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    part_1_time = dt.now()
    circle2 = get_data(is_test)
    lookup_list = run_alt(circle2, int(1e6), int(1e7))
    first_index = lookup_list[1]
    second_index = lookup_list[first_index]
    part_2_answer = second_index * first_index

    diff_time = dt.now() - part_1_time
    print('Part 2: {}'.format(part_2_answer))
    
    print('That took {:.7f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
