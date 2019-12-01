import pandas as pd
import numpy as np
import datetime as dt

def get_data():
    in_file = 'inputs/day01.txt'
    with open(in_file) as f:
        lines = f.readlines()
    return [int(x.strip()) for x in lines]

def get_naive_required_fuel(mass):
    return np.floor(mass/3) - 2

def get_actual_required_fuel(mass, pre_mass = 0):
    next_fuel = get_naive_required_fuel(mass)
    if next_fuel <= 0:
        return pre_mass
    return get_actual_required_fuel(next_fuel, pre_mass + next_fuel)

def main():
    data = np.array(get_data())
    fuel = int(sum(get_naive_required_fuel(data)))
    print('Part 1: Naive fuel requirement: {}'.format(fuel))

    fuel_2 = int(sum([get_actual_required_fuel(x) for x in get_data()]))
    print('Part 2: Actual fuel requirement: {}'.format(fuel_2))

if __name__ == '__main__':
    begin = dt.datetime.now()
    main()
    diff_time = dt.datetime.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
