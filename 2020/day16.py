import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day16.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day16.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]


    params = {}
    your_ticket = []
    nearby_tickets = []
    param_pattern = "^(.*): (\d+)-(\d+) or (\d+)-(\d+)$"
    param_re = re.compile(param_pattern)
    state = 'params'
    for line in lines:
        if line == 'your ticket:':
            state = 'your ticket'
            continue
        elif line == 'nearby tickets:':
            state = 'nearby tickets'
            continue
        if state == 'your ticket' and len(line) > 0:
            your_ticket = [int(x) for x in line.split(',')]
        elif state == 'nearby tickets' and len(line) > 0:
            other_ticket = [int(x) for x in line.split(',')]
            nearby_tickets.append(other_ticket)
        else:
            s = param_re.search(line)
            if s:
                g = s.groups()
                params[g[0]] = [x for x in range(int(g[1]), int(g[2])+1)] + [x for x in range(int(g[3]), int(g[4])+1)]
    return your_ticket, nearby_tickets, params


def part1(nearby_tickets, params):
    valid_ints = set()
    for key in params:
        valid_ints.update(params[key])
    invalid = []
    bad_tickets = []
    for ticket in nearby_tickets:
        for val in ticket:
            if val not in valid_ints:
                invalid.append(val)
                bad_tickets.append(ticket)

    good_tickets = []
    for ticket in nearby_tickets:
        if ticket not in bad_tickets:
            good_tickets.append(ticket)
    print('Part 1: ', sum(invalid))


    columns = np.array(good_tickets).T
    cols = {}
    for i, col in enumerate(columns):
        cols[i] = {}
        cols[i]['values'] = col
        cols[i]['possible_matches'] = [x for x in params.keys()]

    unassigned_params = [x for x in params.keys()]
    assigned_params = []
    matched_cols = {}
    
    while unassigned_params:
        for col_i in cols:
            if col_i in matched_cols:
                continue
            col = cols[col_i]
            for param in assigned_params:
                if param in col['possible_matches']:
                    col['possible_matches'].pop(col['possible_matches'].index(param))
            col_values = set(col['values'])
            for param in unassigned_params:
                if param in col['possible_matches']:
                    p_values = set(params[param])
                
                    if col_values.intersection(p_values) != col_values:
                        # this is not a good parameter match
                        col['possible_matches'].pop(col['possible_matches'].index(param))
            if len(col['possible_matches']) == 1:
                p_match = col['possible_matches'][0]
                matched_cols[col_i] = p_match
                assigned_params.append(unassigned_params.pop(unassigned_params.index(p_match)))
                
    departure_indexes = []
    for col_index in matched_cols:
        if 'departure' in matched_cols[col_index]:
            departure_indexes.append(col_index)
    print('Part 2:', np.prod([my_ticket[x] for x in departure_indexes]))

if __name__ == '__main__':
    begin = dt.now()
    my_ticket, nearby_tickets, params = get_data(False)
    p1 = part1(nearby_tickets, params)
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #p2 = run(data, 30000000)
    #print('Part 2: {}'.format(p2))
    #diff_time = dt.now() - begin
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
