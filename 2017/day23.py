import re
import datetime as dt
from collections import defaultdict

class Thread:
  def __init__(self, program_id):
    self.id = program_id
    self.registers = defaultdict(int)
    for letter in 'abcdefgh':
      self.registers[letter] = 0
    self.instruction_pointer = 0
    self.muls = 0
    self.instructions = None
    self.is_active = True
  def set_register(self, register, value):
    self.registers[register] = value
  def get_number_of_multiplications(self):
    return self.muls
  def set_instructions(self, instructions):
    self.instructions = instructions[:]
  def show_registers(self, additional = ''):
    r = self.registers
    v = str(additional) + ' {} {} {} {} {} {} {} {}'.format(r['a'], r['b'], r['c'], r['d'], r['e'], r['f'], r['g'],r['h'])
    print(v)
  def opcode_fn(self, op_type, Z):
    X, Y = Z
    try:
      Y = int(Y)
    except:
      Y = self.registers[Y]
    try: 
      X = int(X)
    except:
      X = X

    self.instruction_pointer += 1
    if op_type == 'set':
      self.registers[X] = Y
    if op_type == 'sub':
      self.registers[X] -= Y
    if op_type == 'mul':
      self.registers[X] *= Y
      self.muls += 1
    if op_type == 'jnz':
      if type(X) != int:
        X = self.registers[X]
      if X != 0:
        self.instruction_pointer += Y-1

  def perform_instruction(self, verbose=False):
    if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.instructions):
      self.is_active = False
      #print('Thread {} is exiting with instruction pointer value = {}'.format(self.id,
      #self.instruction_pointer))
      return
    instruct = self.instructions[self.instruction_pointer]
    if verbose:
      self.show_registers('{:2} {}'.format(self.instruction_pointer, instruct))
    self.opcode_fn(instruct[0], instruct[1])

def part_a(instructions):
  
  thread = Thread(0)
  thread.set_instructions(instructions)
  while thread.is_active:
    thread.perform_instruction()
  print('Part a: the number of multiplications involved was {}'
  .format(thread.get_number_of_multiplications()))

def part_b(instructions):

  thread1 = Thread(1)

  thread1.set_instructions(instructions)
  thread1.set_register('a', 1)
  while thread1.is_active:
    thread1.perform_instruction(True)
    if thread1.registers['d'] == 12:
      thread1.is_active = False
  thread1.show_registers()

def optimized_b():
  # minor cycle: e is incremented up to b
  # major cycle: d is incremented, also up to b
  # along the way, if b is not prime, there will be combinations of d and e where b = d*e. If this
  # happens, f gets set to zero. If bis not prime, f stays at one through minor and major cycles
  # eventually d gets all the way to b. if b was not prime, then f was set to zero, and so we check
  # for that and increment h by one.
  # then we check to see if b == c. If not, we increment b until it gets to c

  # for our case, b starts at 106700, and is 17000 higher at 123700. So the values of b that were
  # run:

  lower = 106700
  upper = 123700
  b_values = [x for x in range(lower, upper+1, 17)]

  # going to heat for now on the primes
  primes = []
  with open('/Users/rob/Code/ProjectEuler/Primes.txt') as f:
    for line in f:
      x = int(line.strip())
      if x > lower and x < upper+1:
        primes.append(x)

  total_bs = len(b_values)
  n_primes = 0
  for b in b_values:
    if b in primes:
      n_primes += 1

  print('Part b: the value of h at the end is {}'.format(total_bs - n_primes))


def main():
  with open('inputs/day23.txt') as f:
    instructions = [x.strip() for x in f.readlines()]

  instructions = [[x.split()[0], tuple(x.split()[1:])] for x in instructions]
  
  part_a(instructions)
  #part_b(instructions)
  optimized_b()  


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))


