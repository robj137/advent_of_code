import datetime as dt
import re
import numpy as np
from collections import defaultdict, Counter, deque
import operator

def main():
  
  opening_state = ''
  directions = {}
  current_state = ''
  number_of_steps = 0
  predicate_value = 0

  state_dicts = {}
  #with open('inputs/day25.test.txt') as f:
  with open('inputs/day25.txt') as f:
    for line in f:
      if 'Begin in' in line:
        opening_state = re.search('Begin in state ([A-Z]+).', line.strip()).groups()[0]
      if 'Perform a diagnostic' in line:
        number_of_steps = int(re.search('(\d+)', line.strip()).groups()[0])

      if 'In state' in line:
        current_state = re.search('In state ([A-Z]+):', line.strip()).groups()[0]
        state_dicts[current_state] = get_state_dict(current_state)
  
      if 'If the current value is' in line:
        predicate_value = int(re.search('(\d+)', line.strip()).groups()[0])

      if 'Write the value' in line:
        state_dicts[current_state]['write_value'][predicate_value] = int(re.search('(\d+)', line.strip()).groups()[0])
        
      if 'Move one slot' in line:
        if 'left' in line:
          state_dicts[current_state]['move_value'][predicate_value] = -1
        else:
          state_dicts[current_state]['move_value'][predicate_value] = 1

      if 'Continue with state' in line:
        state_dicts[current_state]['next'][predicate_value] = re.search('state ([A-Z]+).', line.strip()).groups()[0]


  #print(opening_state)
  #print(number_of_steps)
  #for key in sorted(state_dicts.keys()):
  #  print(key, state_dicts[key])
  
  cursor = 0
  state = opening_state
  tape = defaultdict(int)
  tape[cursor] = 0
  
  for i in range(number_of_steps):
    cursor, state = take_step(state_dicts, cursor, state, tape)

  print('Part a: Checksum = {}'.format(sum(tape.values())))

def take_step(state_dicts, cursor, state, tape):
  directions = state_dicts[state]
  current_value = tape[cursor]
  tape[cursor] = directions['write_value'][current_value]
  cursor += directions['move_value'][current_value]
  state = directions['next'][current_value]
  return cursor, state

def get_state_dict(state):
  state_dict = {}
  state_dict['label'] = state
  state_dict['write_value'] = [0,0]
  state_dict['move_value'] = [0,0]
  state_dict['next'] = ['', '']
  return state_dict

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

