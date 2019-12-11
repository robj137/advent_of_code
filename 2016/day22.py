import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
import heapq
import pickle

class Node():
    def __init__(self, x, y, size, used, avail, use_perc):
        self.x = x
        self.y = y
        self.size = size
        self.used = used
        self.avail = avail
        self.use_perc = use_perc
        self.up = self.left = self.right = self.down = None
        self.connected = []
        self.contains_payload = False


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
        if target.avail > self.used:
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
        if target.avail > self.used:
            xfer = self.remove()
            if xfer <= target.avail:
                target.add(xfer)
            else:
                self.add(xfer)
                print('Could not xfer {} from {} to {} (only have {} available).'
                    .format(xfer, (self.x, self.y),(target.x, target.y), target.avail) )

class Grid():
    def __init__(self, nodes):
        self.payload_location = None, None
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
                    node.connected.append(node.up)
                if y != y_len - 1:
                    node.down = self.node_map[y+1, x]
                    node.connected.append(node.down)
                if x != 0:
                    node.left = self.node_map[y, x-1]
                    node.connected.append(node.left)
                if x != x_len - 1:
                    node.right = self.node_map[y, x+1]
                    node.connected.append(node.right)
        self.node_map = self.node_map.transpose()

    def get_payload_distance_to_goal(self):
        x, y = self.payload_location
        return x + y

    def set_payload_location(self, x, y):
        self.payload_location = x, y

    def __getitem__(self, key):
        a, b = key
        return self.node_map[a, b]

    def stringify(self):
        return pickle.dumps(self)


    def print(self, metric = 'avail'):
        pic = []
        width, height = self.node_map.shape
        for i in range(height):
            pixel_row = self.node_map[:,i]
            pic.append(['{}/{} '.format(x.used, x.avail + x.used).rjust(7) for x in pixel_row])

        [print(''.join(x)) for x in pic]


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

    def get_viable_pairs(self):
        viable_pairs = []
        for i in range(len(self.node_list)):
            node_a = self.node_list[i]
            for j in range(len(self.node_list)):
                node_b = self.node_list[j]
                if node_a.used and node_b.avail > node_a.used and node_a != node_b:
                    viable_pairs.append((node_a, node_b))
        
        return viable_pairs
         
def get_nodes():
    path = 'inputs/day22.txt'
    #path = 'inputs/day22.test.txt'
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

def optimize_moves(grid_snapshot):
    # the 'target' is when the payload is in its place in the grid (0,0)
    # a state is a snapshot of a grid
    # a valid 'move' between two grid snapshots is a transfer of data from
    # one node to a neighboring node.
    # 
    p1 = (0, grid_snapshot.stringify())
    visited = {}

    heap = []
    heapq.heappush(heap, [0, 0, p1, [p1] ])
    while heap:
        _, path_cost, 
    pass

def get_heuristic(grid_snapshot):
    # manhattan distance to target from current cell
    distance = grid_snapshot.get_payload_distance_to_goal()
    # will almost certainly need a "hint" to 
    return distance


def main():
    nodes = get_nodes()
    grid = Grid(nodes)
    pairs = grid.get_viable_pairs()
    part_1 = len(pairs)
    print("Part 1: Number of viable pairs: {}".format(part_1))
    
    grid.print()
if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
