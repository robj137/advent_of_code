import re
import pandas as pd
import numpy as np
import datetime as dt
import sys

def opcode_fn(type, A, B, C, register):
  if type == 'addr':
    register[C] = register[A] + register[B]
  if type == 'addi':
    register[C] = register[A] + B
  if type == 'mulr':
    register[C] = register[A] * register[B]
  if type == 'muli':
    register[C] = register[A] * B
  if type == 'banr':
    register[C] = register[A] & register[B]
  if type == 'bani':
    register[C] = register[A] & B
  if type == 'borr':
    register[C] = register[A] | register[B]
  if type == 'bori':
    register[C] = register[A] | B
  if type == 'setr':
    register[C] = register[A]
  if type == 'seti':
    register[C] = A
  if type == 'gtir':
    register[C] = 1 if A > register[B] else 0
  if type == 'gtri':
    register[C] = 1 if register[A] > B else 0
  if type == 'gtrr':
    register[C] = 1 if register[A] > register[B] else 0
  if type == 'eqir':
    register[C] = 1 if A == register[B] else 0
  if type == 'eqri':
    register[C] = 1 if register[A] == B else 0
  if type == 'eqrr':
    register[C] = 1 if register[A] == register[B] else 0


def perform_step(i, register, ip_value, ip_register):
  register[ip_register] = ip_value
  opcode_fn(i[0], i[1], i[2], i[3], register)
  ip_value = register[ip_register]
  ip_value += 1
  return ip_value

def easy_way():
  
  r3 = 0
  r4 = 0
  r0 = -1
  previously_seen = []
  while r0 != r4:
    r3 = r4 | 65536
    r4 = 16777215 & (65899 * (16777215 & (16098955 + (255 & r3)))) 
    while r3 >= 256:
      r3 = r3 // 256
      r4 = 16777215 & ( 65899 * ( 16777215 & (r4 + (255 & r3)))) 
    if r4 in previously_seen:
      print('Part 2: Lowest non-negative integer value (most instructions): {}'
              .format(previously_seen[-1]))
      r4 = r0
    else:
      previously_seen.append(r4)
      if len(previously_seen) == 1:
        print('Part 1: Lowest non-negative integer value (fewest instructions): {}'
              .format(previously_seen[-1]))

  print(len(previously_seen))

def main():
  easy_way()
  
  #r0 = 0
  #if len(sys.argv) > 1:
  #  r0 = int(sys.argv[1])
  #ip = -1
  #instructions = []
  #pattern = '([a-z]+) (\d+) (\d+) (\d+)'
  #with open('inputs/day21.txt') as f:
  #  for line in f:
  #    if '#ip' in line:
  #      ip = int(line.split(' ')[1])
  #    if '#ip' not in line:
  #      g = re.search(pattern, line.strip()).groups()
  #      word = g[0]
  #      codes = [int(x) for x in g[1:]]
  #      instruct = [word]
  #      instruct.extend(codes)
  #      instructions.append(instruct)

  #[print(x) for x in instructions]

  #register = [0]*6
  #register[0] = r0
  #ip_register = ip
  #ip_value = 0
  #print(register)
  #n_instructions = 0
  #with open('d21out.txt', 'w') as f:
  #  while ip_value < len(instructions):
  #    n_instructions += 1
#
#      #v = input([n_instructions, ip_value, instructions[ip_value], register])
#      f.write('{} {} {} {}\n'.format(n_instructions, ip_value, instructions[ip_value], register))
#      #if v == 'q':
      #  break
#      ip_value = perform_step(instructions[ip_value], register, ip_value, ip_register)
#      print(register)
#  print(n_instructions)


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
