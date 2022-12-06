import numpy as np
import heapq
import sys
from collections import Counter
from datetime import datetime as dt


class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.position = (x, y)
        self.value = value
        self.neighbors = []
        self.label = ''
        self.heuristic = -1 * (x*x + y*y)**0.5 # closer to end => farther from start, so just use that
        self.heuristic = 0

        self.total_cost = 0

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value


    def __hash__(self):
        return hash((self.position, self.value))



def path_search(data):
    # I guess it's A*? I started with Dijkstra, but modified the heap priority to take into account
    # an heuristic (distance from current cell to the target). This sped up the search from ~ 2
    # minutes to ~ 15 seconds
    nodes, array = data
    p1 = (0,0,'t')
    start = nodes[(0, 0)]
    end = [x for x in filter(lambda x: nodes[x].label == 'end', nodes)][0]
    visited = {}

    heap = []
    heap_cost = 0 # heuristic + path cost
    path_cost = 0 # actual path cost
    heapq.heappush(heap, [heap_cost, path_cost, start, [start]])
    while heap:
      _, path_cost, thisNode, path = heapq.heappop(heap)
      if thisNode not in visited:
        visited[thisNode] = 1
        for node in thisNode.neighbors:
          if node not in visited:
            cost =  node.value 
            sum1 = path_cost + cost
            heap_cost = sum1 + node.heuristic
            heapq.heappush(heap, [path_cost + node.value + node.heuristic, path_cost + node.value, node ,path + [node]])
            if node.label == 'end':
              
              return path_cost + node.value
    return float('inf'), float('inf'), [], [] # didn't work, so return inf


def expand_lines(lines):
    block1 = lines
    block2 = (block1 + 1) % 10 + 1 * ((block1 + 1) % 10 == 0)
    block3 = (block2 + 1) % 10 + 1 * ((block2 + 1) % 10 == 0)
    block4 = (block3 + 1) % 10 + 1 * ((block3 + 1) % 10 == 0)
    block5 = (block4 + 1) % 10 + 1 * ((block4 + 1 ) % 10 == 0)
    block = np.concatenate([block1, block2, block3, block4, block5], axis=0)

    block1 = block
    block2 = (block1 + 1) % 10 + 1 * ((block1 + 1) % 10 == 0)
    block3 = (block2 + 1) % 10 + 1 * ((block2 + 1) % 10 == 0)
    block4 = (block3 + 1) % 10 + 1 * ((block3 + 1) % 10 == 0)
    block5 = (block4 + 1) % 10 + 1 * ((block4 + 1 ) % 10 == 0)
    block = np.concatenate([block1, block2, block3, block4, block5], axis=1)
    return block

def get_data(is_test=True, part2=False):
    path = 'inputs/day15.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()

    lines = np.array([[int(y) for y in x.strip()] for x in lines])
    if part2:
        lines = expand_lines(lines)
    M, N = lines.shape
    nodes = {} # key is tuple
    for i in range(M):
        for j in range(N):
            value = lines[i, j]
            node = Node(i, j, value)
            nodes[(i, j)] = Node(i, j, value)
    for i in range(M):
        for j in range(N):
            neighbor_indices = [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]
            for ndx in neighbor_indices:
                if ndx in nodes:
                    nodes[(i, j)].neighbors.append(nodes[ndx])
            
    nodes[(0, 0)].label = 'start'
    nodes[(M-1, N-1)].label = 'end'
    return nodes, lines

if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1 = path_search(data)
    part1_time = dt.now()
    diff_time = part1_time - begin
    print('Part 1:', part1)
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    data = get_data(is_test, True)
    part2 = path_search(data)
    diff_time = dt.now() - part1_time
    print('Part 2:', part2)
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
