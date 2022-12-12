import numpy as np
import heapq


def get_data():
    with open('inputs/day12.txt') as f:
    #with open('inputs/day12.test.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    d = np.array([list(x) for x in lines])
    X, Y = d.shape
    node_dict = {}
    start_node = end_node = None
    for i in range(X):
        for j in range(Y):
            node_dict[(i, j)] = Node(i, j, d[i,j])
            if node_dict[(i, j)].is_start:
                start_node = node_dict[(i, j)]
            if node_dict[(i, j)].is_end:
                end_node = node_dict[(i, j)]
    for i in range(X):
        for j in range(Y):
            this_index = (i, j)
            neighbor_indexes = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for nbr in neighbor_indexes:
                if nbr in node_dict:
                    if node_dict[nbr].val - node_dict[this_index].val <= 1:
                        node_dict[this_index].valid_neighbors[nbr] = 1
    a_nodes = [node_dict[x] for x in node_dict if node_dict[x].val_char in ['S','a']]
    return node_dict, start_node, end_node, a_nodes

class Node:
    def __init__(self, x, y, val):
        self.pos = (x, y)
        self.valid_neighbors = {}
        self.val = ord(val)
        self.val_char = val
        self.is_start = self.is_end = False
        if val == 'S':
            self.val = ord('a')
            self.is_start = True
        if val == 'E':
            self.val = ord('z')
            self.is_end = True


def path_search(nodes, start, end):
    # It's just Dijkstra
    visited = {}
    heap = []
    path_cost = 0 # actual path cost
    path = [start.pos]
    heapq.heappush(heap, [0, start.pos, []])
    while heap:
      cost, node_ndx, path = heapq.heappop(heap)
      thisNode = nodes[node_ndx]
      if thisNode not in visited:
        visited[thisNode] = 1
        for node in thisNode.valid_neighbors:
          if node not in visited:
            heapq.heappush(heap, [len(path + [node]), node, path + [node]])
            if node == end.pos:
                #return path + [node], len(path + [node])
                return len(path + [node])
    return float('inf')


if __name__ == '__main__':

    #print(node_dict)
    #print(len(node_dict))
    #print('start:', start_node.x, start_node.y)
    #print('end:', end_node.x, end_node.y)
    node_dict, start_node, end_node, a_nodes = get_data()
    print('part 1:', path_search(node_dict, start_node, end_node))
    a_path_values = []
    for node in a_nodes:
        a_path_values.append(path_search(node_dict, node, end_node))
    print('part 2:', min(a_path_values))
