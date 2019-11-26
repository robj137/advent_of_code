import pandas as pd
from datetime import datetime as dt
import re
from itertools import permutations
from iminuit import Minuit
import numpy as np

def get_keys():
    keys = ['children', 'cats', 'samoyeds', 'pomeranians', 'akitas', 'vizslas', 
            'goldfish', 'trees', 'cars', 'perfumes']
    return keys

def get_sued():
    path = 'inputs/day16.txt'
    with open(path) as f:
        lines = f.readlines()
    keys = get_keys()
    pattern1 = 'Sue (\d+): (.*)'
    values = []
    for line in lines:
        result = re.search(pattern1, line)
        if result:
            groups = result.groups()
            name = int(groups[0])
            blank = get_blank_input(name)
            for item in groups[1].split(','):
                kind, count = item.split(':')
                blank[kind.strip()] = int(count.strip())
            values.append(blank)
    df = pd.DataFrame(values).set_index('Sue')
    return df

def get_blank_input(label):
    keys = get_keys()
    blank = {'Sue': int(label)}
    for key in keys:
        blank[key] = None
    return blank

def get_ticker_tape():
    d = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }
    return d

def get_pruned_list(sues, part_2 = False):
    cuts = []
    ticker_tape = get_ticker_tape()
    for t in ticker_tape:
        cut = None
        if part_2 and t in ['cats', 'trees']:
            cut = (sues[t] > ticker_tape[t]) | (sues[t].isna())
        elif part_2 and t in ['pomeranians', 'goldfish']:
            cut = (sues[t] < ticker_tape[t]) | (sues[t].isna())
        else:
            cut = (sues[t] == ticker_tape[t]) | (sues[t].isna())
        cuts.append(cut)
    all_cuts = 1
    for cut in cuts:
        all_cuts = all_cuts & cut
    my_sue = sues[all_cuts]
    return my_sue


def main():
    ticker_tape = get_ticker_tape()
    cuts = []
    sues = get_sued()
    my_sue1 = get_pruned_list(sues)
    my_sue1_number = my_sue1.reset_index()['Sue'][0]
    print('Part 1: Sue #{} got me the gift'.format(my_sue1_number))
    my_sue2 = get_pruned_list(sues, True)
    my_sue2_number = my_sue2.reset_index()['Sue'][0]
    print('Part 2: Sue #{} actually got me the gift'.format(my_sue2_number))



if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
