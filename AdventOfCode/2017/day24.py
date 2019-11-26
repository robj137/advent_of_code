import operator
import datetime as dt
from collections import Counter
import numpy as np

def main():
  with open('inputs/day24.txt') as f:
    components = [list(sorted([int(x.split('/')[0]), int(x.split('/')[1])])) for x in [y.strip() for y in f.readlines()]]

  #[print(x) for x in components]
  #print(components)
  #print(stringify_options(components))
  #print(listify_options(stringify_options(components)))

  valid_bridges = {}
  append_component('', stringify_options(components), 0, valid_bridges)

  #for key in valid_bridges.keys():
  #  print(key, valid_bridges[key])

  print('Part a: maximum value of {} is achieved with path {}'
  .format(max(valid_bridges.values()), max(valid_bridges.items(), key=operator.itemgetter(1))[0]))

  longest_length = 0
  for key in valid_bridges.keys():
    this_length = len(key.split('--'))
    if this_length > longest_length:
      longest_length = this_length
  
  strongest_longest_value = 0
  for key in valid_bridges.keys():
    if len(key.split('--')) == longest_length:
      if valid_bridges[key] > strongest_longest_value:
        strongest_longest_value = valid_bridges[key]
  print('Part b: The longest and strongest bridge has a strength of {}, length of {}'
  .format(strongest_longest_value, longest_length))

def stringify_options(l):
  return '--'.join(['{}/{}'.format(x[0], x[1]) for  x in l])

def listify_options(l):
  components = l.split('--')
  return [[int(x.split('/')[0]), int(x.split('/')[1])] for x in components if len(x) > 0]



def append_component(previous, left, open_port, valid_bridges):
  previous_list = listify_options(previous)
  left_list = listify_options(left)
  for component in left_list:
    if open_port in component:
      next_port = component[1] if component[0] == open_port else component[0]
      added = previous_list[:]
      subtracted = left_list[:]
      added.append(component)
      subtracted.pop(subtracted.index(component))
      append_component(stringify_options(added), stringify_options(subtracted), next_port, valid_bridges)
  valid_bridges[previous] = sum([sum(x) for x in previous_list])
  #print(previous)

      

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

