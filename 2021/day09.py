import numpy as np
import sys
import re
from collections import defaultdict, Counter

class Node:
    def __init__(self, x, y, val):
        self.val = val
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.neighbors = []

def get_data(is_test=True):
    path = 'inputs/day09.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    lines = [[int(x) for x in list(x.strip())] for x in lines]  
    return np.array(lines)


def get_nodes(data):
    nodes = {}
    M, N = data.shape
    for i in range(M):
        for j in range(N):
            if data[i,j] == 9:
                # not in the basin
                continue
            node = Node(i, j, data[i, j])
            if i-1 >= 0:
                if data[i-1, j] != 9:
                    node.neighbors.append((i-1, j))
            if i+1 < M:
                if data[i+1, j] != 9:
                    node.neighbors.append((i+1, j))
            if j-1 >= 0:
                if data[i, j-1] != 9:
                    node.neighbors.append((i, j-1))
            if j+1 < N:
                if data[i, j+1] != 9:
                    node.neighbors.append((i, j+1))
            nodes[(i, j)] = node
    return nodes    

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    print(data)
    M, N = data.shape
    lows = {}
    for i in range(M):
        for j in range(N):
            neighbors = []
            if i-1 >= 0:
                neighbors.append(data[i-1, j])
            if i+1 < M:
                neighbors.append(data[i+1, j])
            if j-1 >= 0:
                neighbors.append(data[i, j-1])
            if j+1 < N:
                neighbors.append(data[i, j+1])
            if (data[i, j] < np.array(neighbors)).all():
                lows[(i, j)] = data[i,j]
    print(len(lows))
    print(sum([int(lows[x]) + 1 for x in lows]))
    
    nodes = get_nodes(data)
    basins = {}
    node_keys = [x for x in nodes.keys()]
    mapped = []
    while node_keys:
        this_basin = []
        this_low = None
        key = node_keys.pop()
        node = nodes[key]
        queue = [node]
        while queue:
            this_node = queue.pop()
            if this_node.pos in lows:
                this_low = this_node.pos
            if this_node.pos in node_keys:
                node_keys.pop(node_keys.index(this_node.pos))
            this_basin.append(this_node)
            for neighbor in this_node.neighbors:
                neighbor_node = nodes[neighbor]
                if neighbor_node not in queue and neighbor_node.pos in node_keys:
                    queue.append(neighbor_node)     
        # end of queue, so we should have crawled through each node
        basins[this_low] = this_basin

    basin_lengths = [len(basins[x]) for x in basins]
    basin_lengths = sorted(basin_lengths)[::-1]
    print(np.prod(basin_lengths[0:3]))
    #print(nodes.keys())
