import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict

class Node():
    def __init__(self, x, y, size, used, avail, use_perc):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.use_perc = use_perc
        self.up = self.left = self.right = self.down = None
    
    def get_avail(self):
        return self.avail

    def add(self, x):
        if x < self.avail:
            self.used += x
            self.avail -= x

    def remove(self):
        self.avail = self.size
        used = self.used
        self.used = 0
        return used

    def print(self):
        print('{} {} {} {} {}'.format(self.x, self.y, self.size, self.used, self.avail))

    def receive(self, neighbor):
        target = None
        if neighbor == 'up':
            target = self.up
        if neighbor == 'down':
            target = self.down
        if neighbor == 'left':
            target = self.left
        if neighbor == 'right':
            target = self.right
        if target.get_avail() > self.used:
            xfer = target.remove()
            if xfer <= self.avail:
                self.add(xfer)
            else:
                target.add(xfer)
                print('Could not xfer {} from {} to {} (only have {} available).'
                    .format(xfer, (target.x, target.y),(self.x, self.y), self.avail) )

    def send(self, neighbor):
        target = None
        if neighbor == 'up':
            target = self.up
        if neighbor == 'down':
            target = self.down
        if neighbor == 'left':
            target = self.left
        if neighbor == 'right':
            target = self.right
        if target.get_avail() > self.used:
            xfer = self.remove()
            if xfer <= target.avail:
                target.add(xfer)
            else:
                self.add(xfer)
                print('Could not xfer {} from {} to {} (only have {} available).'
                    .format(xfer, (self.x, self.y),(target.x, target.y), target.avail) )

class Grid():
    def __init__(self, nodes):
        x_len, y_len = self.get_extent(nodes)
        self.node_map = [[None] * x_len]*y_len
        self.node_map = np.array(self.node_map)
        self.node_list = []
        for data in nodes:
            x, y = data
            x = int(x[1:])
            y = int(y[1:])
            lookup = nodes[data]
            size = lookup['Size']
            used = lookup['Used']
            avail = lookup['Avail']
            node = Node(x, y, size, used, avail, 0)
            self.node_map[y, x] = node
            self.node_list.append(node)
        for x in range(x_len):
            for y in range(y_len):
                node = self.node_map[y, x]
                if y != 0:
                    node.up = self.node_map[y-1, x]
                if y != y_len - 1:
                    node.down = self.node_map[y+1, x]
                if x != 0:
                    node.left = self.node_map[y, x-1]
                if x != x_len - 1:
                    node.right = self.node_map[y, x+1]
    
    def __getitem__(self, key):
        a, b = key
        return self.node_map[b, a]

    def get_extent(self, nodes):
        x_max = y_max = 0
        for a, b in nodes:
            x = int(a[1:])
            y = int(b[1:])
            if x_max < x:
                x_max = x
            if y_max < y:
                y_max = y
        return x_max+1, y_max+1


def get_nodes():
    path = 'inputs/day22.txt'
    with open(path) as f:
        lines = f.readlines()
    tops = lines[0:2]
    lines = lines[2:]
    pattern = '/dev/grid/node-(x\d+)-(y\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)\%'
    nodes = {}
    for line in lines:
        result = re.search(pattern, line)
        if result:
            g = result.groups()
            nodes[(g[0], g[1])] = {'Size': int(g[2]), 'Used': int(g[3]), 'Avail': int(g[4]), 'Use%': int(g[5])}
        else:
            print('wtf', line)

    return nodes

def get_viable_pairs(nodes):
    node_keys = [x for x in nodes.keys()]
    n_pairs = []
    for key in node_keys:
        node = nodes[key]
        for key2 in node_keys:
            node2 = nodes[key2]
            if key != key2 and node['Used'] != 0 and node['Used'] < node2['Avail']:
                n_pairs.append((key, key2))
    return n_pairs

def check_connected(pair):
    a, b = pair
    ax = int(a[0][1:])
    ay = int(a[1][1:])
    bx = int(b[0][1:])
    by = int(b[1][1:])
    if abs(ax-bx) == 1 and abs(ay-by) == 0 or abs(ax-bx) == 0 and abs(ay-by) == 1:
        return True
    return False

def get_viable_conected_pairs(nodes):
    pairs = get_viable_pairs(nodes)
    connected = []
    for pair in pairs:
        if check_connected(pair):
            connected.append(pair)
    return connected

def part1():
    nodes = get_nodes()
    pairs = get_viable_pairs(nodes)
    print(len(pairs))
    for a, b in pairs:
        if b != ('x35', 'y18'):
            print(a,b)


def part2():
    nodes = get_nodes()
    
    connected = get_viable_conected_pairs(nodes)
    print(connected)

    grid = Grid(nodes)

def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
