import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict


def get_inputs():
    with open('inputs/day19.txt') as f:
    #with open('inputs/day19_alt.txt') as f:
        lines = f.readlines()

    molecule = ''
    swaps = []
    for line in lines:
        if '=>' in line:
            swaps.append(line.strip())
        elif len(line) > 1 and '=>' not in line:
            molecule = line.strip()

    swap_dict = defaultdict(list)
    pattern = '([A-Z]?[a-z]?) => (.*)'
    for line in swaps:
        result = re.search(pattern, line)
        if result:
            g = result.groups()
            swap_dict[g[0]].append(g[1])
    return molecule, swap_dict

def get_reverse_dict(d):
    # can't just return {v: k for k, v in d.items()}
    # because values are lists
    r_d = {}
    for key in d.keys():
        for variant in d[key]:
            r_d[variant] = key
    return r_d


def part1(molecule, swap_dict):
    print(molecule)

    replacement_dict = defaultdict(int)

    for swap in swap_dict:
        for variant in swap_dict[swap]:
            indexes = [(x.start(), x.end()) for x in re.finditer(swap, molecule)]
            for a, b in indexes:
                new_r = molecule[:a] + variant + molecule[b:]
                replacement_dict[new_r] += 1

    print('Part 1: Number of distinct molecules: {}'.format(len([x for x in replacement_dict])))

def prune(m, counter, swap_dict, step_dict, seen):
    if m == 'e':
        step_dict[counter] += 1
        print('Part 2: Least number of steps to create molecule = {}'.format(counter))
        return
    if step_dict and counter >= max(step_dict):
        # already gone over an established good step length
        return
    if m in seen and seen[m] >= counter:
        # don't need to do more work than necessary
        # also only keep the branch if the counter is lower than already seen
        return
    seen[m] = counter
    counter += 1
    for key in swap_dict:
        # find indexes of possible swaps
        indexes = [(x.start(), x.end()) for x in re.finditer(key, m)]
        # then do the replacement dance and call prune again with the reduced molecule
        for a, b in indexes:
            new_m = m[:a] + swap_dict[key] + m[b:]
            #print('  ', a, b, key, ':', swap_dict[key], '   ', m, '->', new_m)
            prune(new_m, counter, swap_dict, step_dict, seen)


def part2(molecule, swap_dict):
    # FIXME, because this 'works', but not ideally. (it doesn't actually finish, or if it does, it takes a while)
    # once a valid deconstruction is found, record the number of steps here
    step_dict = defaultdict(int) 
    counter = 0
    seen = {}
    prune(molecule, counter, swap_dict, step_dict, seen)
    # need to recurse! give the molecule and the swap dict (and a counter, and a step dict, and a seen dict
    


def main():
    molecule, swap_dict = get_inputs()
    part1(molecule, swap_dict)

    reverse_swap_dict = get_reverse_dict(swap_dict)

    part2(molecule, reverse_swap_dict)


if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
