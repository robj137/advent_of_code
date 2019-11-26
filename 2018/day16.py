import re
import pandas as pd
import numpy as np
import datetime as dt


def opcode_fn(type, A, B, C, registers):
  if type == 'addr':
    registers[C] = registers[A] + registers[B]
  if type == 'addi':
    registers[C] = registers[A] + B
  if type == 'mulr':
    registers[C] = registers[A] * registers[B]
  if type == 'muli':
    registers[C] = registers[A] * B
  if type == 'banr':
    registers[C] = registers[A] & registers[B]
  if type == 'bani':
    registers[C] = registers[A] & B
  if type == 'borr':
    registers[C] = registers[A] | registers[B]
  if type == 'bori':
    registers[C] = registers[A] | B
  if type == 'setr':
    registers[C] = registers[A]
  if type == 'seti':
    registers[C] = A
  if type == 'gtir':
    registers[C] = 1 if A > registers[B] else 0
  if type == 'gtri':
    registers[C] = 1 if registers[A] > B else 0
  if type == 'gtrr':
    registers[C] = 1 if registers[A] > registers[B] else 0
  if type == 'eqir':
    registers[C] = 1 if A == registers[B] else 0
  if type == 'eqri':
    registers[C] = 1 if registers[A] == B else 0
  if type == 'eqrr':
    registers[C] = 1 if registers[A] == registers[B] else 0

def get_test_entry(r1, r2, instructions):
  test = {}
  test['register1'] = r1
  test['register2'] = r2
  test['instructions'] = instructions
  test['n_matches'] = 0
  test['matches'] = []
  return test

def get_unclaimed_ops(op_dict):
  n_unclaimed = 0
  for op in op_dict:
    if op_dict[op] < 0:
      n_unclaimed += 1
  return n_unclaimed

def main():
  infile = 'inputs/day16.txt'
  tests = []
  before = []
  after = []
  instructions = []
  pattern = '(\d+),* (\d+),* (\d+),* (\d+)'
  with open(infile) as f:
    for line in f:
      if 'Before' in line:
        before = [int(x) for x in re.search(pattern, line).groups()]
      if 'After' in line:
        after = [int(x) for x in re.search(pattern, line).groups()]
        test = get_test_entry(before[:], after[:], instructions[0][:])
        tests.append(test)
        instructions = []
      if len(line) > 5 and 'Before' not in line and 'After' not in line:
        instructions.append([int(x) for x in re.search(pattern, line).groups()])
  ops = ['addr','addi','mulr','muli','banr','bani','borr','bori','setr','seti','gtir','gtri','gtrr','eqir','eqri','eqrr']
  ops_dict = {}
  for op in ops:
    ops_dict[op] = -1

  for test in tests:
    instructs = test['instructions']
    result = test['register2']
    for op in ops:
      reg_copy = test['register1'][:]
      opcode_fn(op, instructs[1], instructs[2], instructs[3], reg_copy)
      if reg_copy == result:
        test['n_matches'] += 1
        test['matches'].append(op)

  n_matchy_tests = 0
  for test in tests:
    if test['n_matches'] >= 3:
      n_matchy_tests += 1

  print('Part a: Found {} tests that had >= 3 similar ops'.format(n_matchy_tests))
  
  while get_unclaimed_ops(ops_dict) > 0:
    for test in tests:
      if test['n_matches'] == 1:
        ops_dict[test['matches'][0]] = test['instructions'][0]
    
    for test in tests:
      for op in ops_dict:
        if ops_dict[op] > -1:
          if op in test['matches']:
            test['matches'].pop(test['matches'].index(op))
            test['n_matches'] -= 1

  register = [0,0,0,0]

  # just reverse the dictionary
  ops_dict = {x: y for y, x in ops_dict.items()}
  for line in instructions:
    op = ops_dict[line[0]]
    opcode_fn(op, line[1], line[2], line[3], register)
  print('Part b: after following instructions, the first register value is now {}'
        .format(register[0]))


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
