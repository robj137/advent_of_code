from datetime import datetime as dt
import sys
import numpy as np

class Orbit:
    def __init__(self, name, parent_name):
        self.name = name
        self.parent_name = parent_name

        self.parent = None
        self.children = []

    def count_parent_orbits(self):
        pointer = self.parent
        n_orbits = 0
        while pointer:
            pointer = pointer.parent
            n_orbits += 1
        return n_orbits

    def get_distance_to_parent(self, parent_name):
        if type(parent_name) != str:
            parent_name = parent_name.name
        n_orbits = 0
        pointer = self.parent
        while pointer:
            n_orbits += 1
            if pointer.name == parent_name:
                return n_orbits
            pointer = pointer.parent
        return np.nan

    def get_parent_orbits(self):
        parents = []
        node = self.parent
        while node:
            parents.append(node)
            node = node.parent
        return parents


def get_data():
    in_file = 'inputs/day06.test.txt'
    in_file = 'inputs/day06.txt'
    with open(in_file) as f:
        entries = [x.strip().split(')') for x in f.readlines()]

    orbit_dict = {}
    orbit_dict['COM'] = Orbit('COM', None)
    for parent, child in entries:
        orbit_dict[child] = Orbit(child, parent)

    for orbit_key in orbit_dict:
        orbit = orbit_dict[orbit_key]
        if orbit.parent_name:
            orbit.parent = orbit_dict[orbit.parent_name]
            orbit_dict[orbit.parent_name].children.append(orbit)

    return orbit_dict



def get_common_node(data, a, b):
    a_parents = reversed(a.get_parent_orbits())
    b_parents = reversed(b.get_parent_orbits())
    
    nearest_common_node = None
    for node in a_parents:
        if node in b_parents:
            nearest_common_node = node
    return nearest_common_node

def main():
    data = get_data()
    n_orbits = 0
    for orbit_name in data:
        orbit = data[orbit_name]
        n_orbits += orbit.count_parent_orbits()
    
    print('Part 1: {}'.format(n_orbits))
    
    common_node = get_common_node(data, data['SAN'], data['YOU'])
    distance_to_travel = 0
    distance_to_travel += data['SAN'].get_distance_to_parent(common_node)
    distance_to_travel += data['YOU'].get_distance_to_parent(common_node)
    distance_to_travel += -2 # b.c. only moving from YOU.parent to SAN.parent
    print('Part 2: {}'.format(distance_to_travel))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
