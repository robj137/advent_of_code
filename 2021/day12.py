import numpy as np
import sys
from collections import Counter

import aoc_utils

class Node:
    def __init__(self, label):
        self.label = label
        self.neighbors = set()
        self.is_start = True if label == 'start' else False
        self.is_end = True if label == 'end' else False
        self.is_upper = True if label == label.upper() else False

class Cluster:
    def __init__(self, rule_type = 'A'):
        self.node_dict = {}
        self.rule_A = True if rule_type == 'A' else False
    def add_node(self, label):
        self.node_dict[label] = Node(label)
    def gimme_node(self, label):
        if label not in self.node_dict:
            self.add_node(label)
        return self.node_dict[label]
    def __call__(self, label):
        return self.node_dict[label]


class Path:
    def __init__(self, cluster, route=['start']):
        self.cluster = cluster
        self.rule_A = cluster.rule_A 
        self.set_route(route)
    def set_route(self, route):
        self.route = route
        self.check()
    def check_proposed_next_stop(self, next_stop):
        next_node = self.cluster(next_stop)
        if next_node.is_start:
            return False
        if next_node.is_upper or next_stop not in self.stop_counter:
            return True
        # so now we know it's lower and there is already one there.
        if self.rule_A:
            return False
        if self.has_double_small:
            return False
        return True
    def check(self):
        self.current_node = self.cluster(self.route[-1])
        self.next_options = self.current_node.neighbors
        self.stop_counter = Counter(self.route)
        small_keys = [x for x in filter(lambda x: not self.cluster(x).is_upper, self.stop_counter.keys()) ]
        small_counts = np.array([self.stop_counter[x] for x in small_keys])
        self.has_double_small = True if np.sum(small_counts == 2) == 1 else False
        self.next_options = [x for x in self.next_options if self.check_proposed_next_stop(x.label)]
    

def get_data(is_test=True, rule_type='A'):
    path = 'inputs/day12.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    cluster = Cluster(rule_type)
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        label_a, label_b = line.strip().split('-')
        node_a = cluster.gimme_node(label_a)
        node_b = cluster.gimme_node(label_b)
        node_a.neighbors.add(node_b)
        node_b.neighbors.add(node_a)
    return cluster

class PathRepo:
    def __init__(self, cluster):
        self.cluster = cluster
        self.spares = []
        self.n_allocated = 0
    def get_path(self, route):
        if self.spares:
            path = self.spares.pop()
            path.set_route(route)
        else:
            path = Path(self.cluster, route)
            self.n_allocated += 1
        return path

    def retire_path(self, path):
        self.spares.append(path)

@aoc_utils.timer
def run_scan(is_test, rule_type):
    cluster = get_data(is_test, rule_type)
    routes = []
    path_repo = PathRepo(cluster)
    queue = []
    p = path_repo.get_path(['start'])
    queue.append(p)
    while queue:
        p = queue.pop()
        if p.current_node.is_end:
            routes.append(p.route)
        else:
            for o in p.next_options:
                route = p.route[:] + [o.label]
                p_new = path_repo.get_path(route)
                queue.append(p_new)
        path_repo.retire_path(p)
    print("maximum paths alocated was", path_repo.n_allocated)
    return len(routes)

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    part1 = run_scan(is_test, 'A')
    print('Part 1:', part1)
    part2 = run_scan(is_test, 'B')
    print('Part 2:', part2)
