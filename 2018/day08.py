import pandas as pd
import numpy as np
import datetime as dt

node_dict = {}

def main():
  numbers = []
  with open('inputs/day8.txt') as f:
    numbers = [int(x) for x in f.read().strip().split(' ')]

  
  # create the tree
  create_node_from_list(numbers, 0)
  #create_node_from_list(get_test_data(), 0)

  tree = node_dict[0]
  
  sum_of_metadata = sum([sum(node_dict[x]['metadata']) for x in node_dict])
  tree_value = get_value(tree)
  print('Part a: Sum of all metadata: {}'.format(sum_of_metadata))
  print('Part b: Value of root node: {}'.format(tree_value))

def get_value(node):
  value = 0
  if node['n_children'] == 0:
    value = sum(node['metadata'])
  else:
    for ndx in node['metadata']:
      if (ndx-1) < node['n_children']:
        value += get_value(node_dict[node['child_indices'][ndx-1]])
  return value

def create_node(address):
  node = {}
  node['address'] = address
  node_dict[address] = node
  return node

def get_test_data():
  data = [2,3,0,3,10,11,12,1,1,0,1,99,2,1,1,2]
  return data

def create_node_from_list(numbers, start):
  # fun with recursion
  # just give it the array reference, and the beginning index
  # 
  # it will register itself in the node_dict
  # it will figure out how many children it has, 
  # it will recursively deal with its children, and from their overall lengths, find its metadata
  # and the overall length of the node
  # 
  # it will return the start of the node and the length of the node
  node = create_node(start)
  child_node_indices = []
  child_lengths = []
  n_child_nodes = numbers[start]
  metadata_length = numbers[start+1]
  node['n_children'] = n_child_nodes
  while n_child_nodes > len(child_node_indices):
    child_index, length = create_node_from_list(numbers, start + 2 + sum(child_lengths))
    child_node_indices.append(child_index)
    child_lengths.append(length)
  node['child_indices'] = child_node_indices
  metadata_start = start + 2 + sum(child_lengths)
  metadata_end = metadata_start + metadata_length
  node['metadata'] = numbers[metadata_start:metadata_end]
  this_node_length = metadata_end - start
  
  return start, this_node_length


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
