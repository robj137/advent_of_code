import numpy as np
import re
import sys
import json
from collections import Counter
from copy import deepcopy
import aoc_utils

def get_data(is_test=True):
    path = 'inputs/day18.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    return [Node(json.loads(x.strip())) for x in lines]

class Node:
    def __init__(self, s=None, parent=None):
        self.parent = parent
        self.value = self.left = self.right = None
        if type(s) == type(None):
            pass
        elif type(s) == int:
            self.value = s
        else:
            a, b = s
            self.left = Node(a, self)
            self.right = Node(b, self)
    def get_depth(self):
        if not self.parent:
            return 0
        return 1 + self.parent.get_depth()
    def is_left(self):
        return True if self.parent and self.parent.left == self else False
    def is_right(self):
        return True if self.parent and self.parent.right == self else False

    def to_string(self):
        if self.value is not None:
            return '{}'.format(self.value)
        return '[{},{}]'.format(self.left.to_string(), self.right.to_string())

def in_order(node, stack):
    if node.value is not None:
        stack.append(node)
        return
    return in_order(node.left, stack), in_order(node.right, stack)

def check_4_depth(node):
    if not node:
        return
    if node.get_depth() == 4 and node.value is None:
        return node
    left_check = check_4_depth(node.left)
    if left_check:
        return left_check
    right_check = check_4_depth(node.right)
    if right_check:
        return right_check

def check_single_digit_values(node):
    if not node:
        return
    if node.value and node.value > 9:
        return node
    left_check = check_single_digit_values(node.left)
    if left_check:
        return left_check
    right_check = check_single_digit_values(node.right)
    if right_check:
        return right_check
            

def reduce(root):
    stack = []
    in_order(root, stack)
    to_explode = check_4_depth(root)
    to_split = check_single_digit_values(root)
    if to_explode:
        explode(to_explode)
        return reduce(root)
    elif to_split:
        sf_split(to_split)
        return reduce(root)
    else:
        # no need to reduce
        return root

def get_root(node):
    if not node.parent:
        return node
    return get_root(node.parent)

def explode(node):
    # this particular node should have no value, but should have a left and right
    root = get_root(node)
    stack = []
    in_order(root, stack)
    ndx_left = stack.index(node.left)
    ndx_right = stack.index(node.right)
    left_fill = stack[ndx_left-1] if ndx_left > 0 else None
    right_fill = stack[ndx_right+1] if ndx_right < len(stack) - 1 else None
    if left_fill:
        left_fill.value += node.left.value
    if right_fill:
        right_fill.value += node.right.value
    node.value = 0
    node.left = node.right = None

def sf_split(el):
    el.left = Node(int(np.floor(el.value/2)), parent=el)
    el.right = Node(int(np.ceil(el.value/2)), parent=el)
    el.value = None

def add(n1, n2, do_reduce=True):
    root = Node()
    root.left = n1
    root.right = n2
    n1.parent = root
    n2.parent = root
    return reduce(root) if do_reduce else root

def get_magnitude(node):
    if node.value is not None:
        return node.value
    return 3 * get_magnitude(node.left) + 2 * get_magnitude(node.right)

@aoc_utils.timer
def run1(nodes):
    s = nodes.pop(0)
    while nodes:
        s = add(s, nodes.pop(0))
    print(s.to_string())
    print(get_magnitude(s))

@aoc_utils.timer
def run2(nodes):
    pristine = deepcopy(nodes)
    magnitudes = []
    for n1 in pristine:
        for n2 in pristine:
            if n1 != n2:
                s = add(deepcopy(n1), deepcopy(n2))
                magnitudes.append(get_magnitude(s))
    print(max(magnitudes))

if __name__ == '__main__':
    
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    nodes1 = get_data(is_test)
    run1(nodes1)
    nodes2 = get_data(is_test)
    run2(nodes2)
