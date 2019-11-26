import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict


def get_input(test=False):
    with open('inputs/day24.txt') as f:
        lines = f.readlines()
    packages = [int(x.strip()) for x in lines]
    if test:
        packages = [1,2,3,4,5,7,8,9,10,11]
    return packages

def add_package(package, weight_list, orderings, packages_left, group_dict):
    if package:

        if len(weight_list) > 6:
            # we know we can do at least as good as 6
            return
        packages_left.pop(packages_left.index(package))
        weight_list.append(package)
        weight_list.sort()
        if tuple(weight_list) in orderings:
            return
        orderings[tuple(weight_list)] += 1
        weight = sum(weight_list)
        non_weight = sum(packages_left)
        if weight * 3 == non_weight:
            # hooray!
            group_dict[len(weight_list)].append(sorted(weight_list[:]))
        if weight * 3 > non_weight:
            #no bueo
            return
    for package in packages_left:
        add_package(package, weight_list[:], orderings, packages_left[:], group_dict)
        


def main():
    packages = get_input(False)
    print(packages)
    print('sum of packages is {}'.format(sum(packages)))
    print(' and a 3rd of that is {}'.format(sum(packages)/3))

    weight_list = []
    packages_left = packages
    group_dict = defaultdict(list)

    orderings = defaultdict(int)
    add_package(None, weight_list, orderings, packages_left, group_dict)


    min_packages = min(group_dict)
    print(min_packages, group_dict[min_packages])

    min_qe = min([np.prod(x) for x in group_dict[min_packages]])

    print('Part 1: the fewest number of packages that can fit is {}'.format(min_packages))
    print('        and the quantum entanglement is {}'.format(min_qe))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
