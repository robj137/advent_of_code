import re
import numpy as np
import datetime as dt

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

def main():
  ip = -1
  instructions = []
  pattern = '([a-z]+) (\d+) (\d+) (\d+)'
  with open('inputs/day19.txt') as f:
    for line in f:
      if '#ip' in line:
        ip = int(line.split(' ')[1])
      if '#ip' not in line:
        g = re.search(pattern, line.strip()).groups()
        word = g[0]
        codes = [int(x) for x in g[1:]]
        instruct = [word]
        instruct.extend(codes)
        instructions.append(instruct)

  register = [0]*6
  ip_register = ip
  ip_value = 0
  ##############################################################
  #     UNCOMMENT for the 'real' version of part a:            #
  ##############################################################
  #print(register)
  #while ip_value < len(instructions):
  #  ip_value = perform_step(instructions[ip_value], register, ip_value, ip_register)
  #  print(ip_value, register)
  #print('Part a: Register 0 is {}'.format(register[0]))
  ##############################################################

  # Part a (the real way) takes about 30 seconds on my machine (a 2013 MacBook Air)
  # Register # 2 (the third one) is equal to 954, and this seems to be what the the other counters
  # in the register are counting up to. ANd they get there, in 7284757 operations. 
  # Atttempting Part b this way seems hopeless, because register 2 is now 10551354. So we have to
  # be more 'clever'. Or maybe just cheat. The way we cheat is to notice how register 0 changes as
  # Part a progresses. Every time the op value = 7, register 0 gets changed, and the way it's
  # chnaged is by adding register 4. But something funny happens, because register 4 and register 5
  # seem linked whenever this happens. In fact, it looks like op value = 7 whenever register 4 *
  # register 5 == register 2. This is just factorization! At the end of the run, register 0 is the
  # sum of all the factors of register 2: sum([1, 2, 3, 6, 9, 18, 53, 106, 159, 318, 477, 954]) =
  # 2106. 

  # The 'cheating' way:

  # Part a
  register = [0]*6
  ip_register = ip
  ip_value = 0
  r2 = get_cheating_value(instructions, ip_value, ip_register, register)
  factors_a = []
  for i in range(1, r2+1):
    if r2/i == int(r2/i):
      factors_a.append(i)

  print('Part a: Register 0 is {}'.format(sum(factors_a)))
  
  register = [0]*6
  register[0] = 1
  ip_register = ip
  ip_value = 0
  r2 = get_cheating_value(instructions, ip_value, ip_register, register)
  factors_b = []
  for i in range(1, r2+1):
    if r2/i == int(r2/i):
      factors_b.append(i)
  print('Part b: Register 0 is {}'.format(sum(factors_b)))


def get_cheating_value(instructions, ip_value, ip_register, register):
  i = 0
  while ip_value < len(instructions):
    i += 1
    ip_value = perform_step(instructions[ip_value], register, ip_value, ip_register)
    if i == 50:
      break
  return register[2]


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
