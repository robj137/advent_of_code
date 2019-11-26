import pandas as pd
from datetime import datetime as dt
from collections import defaultdict
from math import factorial

def get_inputs():
    path = 'inputs/day17.txt'
    with open(path) as f:
        lines = f.readlines()
    containers = [int(x.strip()) for x in lines]
    #containers = [20, 15, 10, 5, 5]
    containers.sort(reverse=True)
    return containers

def add_container(container, volume_left, path, containers_left, path_dict):
    # alrady checked if there is at least enough volume left to fill container
    # first pop the container though
    containers_left.pop(containers_left.index(container))

    path += str(container)
    volume_left -= container

    # now check if we're done or not
    if volume_left == 0:
        sig = tuple(sorted([int(x) for x in path.split('-')]))
        path_dict[sig] += 1
        
        return

    # not done, keep adding to containes
    for new_container in containers_left:
        if new_container <= volume_left:
            add_container(new_container, volume_left, path + '-', containers_left[:], path_dict)

    # if we've come here, then nothing else to do
    return

def main():
    containers = get_inputs()
    volume = 150
    if len(containers) == 5:
        volume = 25
    print(containers)
    path_dict = defaultdict(int)
    path = ''
    containers_left = containers[:]
    for container in containers_left:
        add_container(container, volume, path, containers_left[:], path_dict)

    combos = 0
    combo_dict = defaultdict(int)
    for key in path_dict:
        combos += path_dict[key] // factorial(len(key))
        print(key, path_dict[key], path_dict[key] // factorial(len(key)))
        combo_dict[len(key)] += path_dict[key] // factorial(len(key))

    print('Part 1: Number of combos is {}'.format(combos))
    min_containers = min([int(x) for x in combo_dict.keys()])
    print('Part 2: Number of ways to use {} containers is {}'
            .format(min_containers, combo_dict[min_containers]))


if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
