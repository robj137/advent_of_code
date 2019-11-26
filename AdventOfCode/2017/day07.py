import datetime as dt
from collections import defaultdict, Counter

def fill_weights(node_name, program_dict, order = 0):
  # want to traverse the tree from root to leaves
  # add two fields to the node
  # an array of the weight of its children (child_weights), in same order as children array
  # total weight, = itself + sum(child_weights)
  node = program_dict[node_name]
  node['child_weights'] = []
  node['order'] = order
  while len(node['child_weights']) < len(node['children']):
    child_index = len(node['child_weights'])
    node['child_weights'].append(fill_weights(node['children'][child_index], program_dict, order+1))

  node['total_weight'] = node['weight'] + sum(node['child_weights'])
  return node['total_weight']

def main():
  instructions = []
  with open('inputs/day7.txt') as f:
    for line in f:
      instructions.append(line.strip())
  program_dict = defaultdict(str)
  for program in instructions:
    name = program.split(' (')[0]
    weight = int(program.split('(')[1].split(')')[0])
    if '->' in program:
      children = [x.strip() for x in program.split('->')[1].split(',')]
    else:
      children = []
    program_dict[name] = {'weight':weight, 'children':children, 'parent':'', 'balanced':True}

  for program in program_dict:
    for child in program_dict[program]['children']:
      program_dict[child]['parent'] = program
  
  root_program = ''
  for program in program_dict:
    if not program_dict[program]['parent']:
      root_program = program
      print('Part a: The root program is {}'.format(program))

  fill_weights(root_program, program_dict)

  for program in program_dict:
    node = program_dict[program]
    weights = node['child_weights']
    if weights:
      if weights != [weights[0]]*len(weights):
        node['balanced'] = False
      
  unbalanced = []
  max_order = 0
  unbalanced_parent=''
  for program in program_dict:
    if not program_dict[program]['balanced']:
      if program_dict[program]['order'] > max_order:
        unbalanced_parent = program
        max_order = program_dict[program]['order']

  unbalanced_parent_node = program_dict[unbalanced_parent]
  c = Counter(unbalanced_parent_node['child_weights'])
  wrong_weight = 0
  right_weight = 0
  for key in c:
    if c[key] == 1:
      wrong_weight = key
    else:
      right_weight = key
  diff = right_weight - wrong_weight
  wrong_index = unbalanced_parent_node['child_weights'].index(wrong_weight)
  unbalanced_node = program_dict[unbalanced_parent_node['children'][wrong_index]]
  print('Part b: the node {}, which weighs {}, needs to weigh {} instead'.format(
    unbalanced_parent_node['children'][wrong_index],
    unbalanced_node['weight'], 
    unbalanced_node['weight'] + diff))

if __name__ == '__main__':                                                                                                                             
  begin = dt.datetime.now()                                                                                                                            
  main()                                                                                                                                               
  diff_time = dt.datetime.now() - begin                                                                                                                
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))                                                            

