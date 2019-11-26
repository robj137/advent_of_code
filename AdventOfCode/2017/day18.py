import re
import datetime as dt
from collections import defaultdict

class Thread:
  def __init__(self, program_id):
    self.id = program_id
    self.registers = defaultdict(int)
    self.registers['p'] = program_id
    self.queue = []
    self.partner = None
    self.instruction_pointer = 0
    self.sends = []
    self.receives = []
    self.instructions = None
    self.is_waiting = False
    self.is_exited = False
  def is_active(self):
    return not self.is_exited and not self.is_waiting
  def set_instructions(self, instructions):
    self.instructions = instructions[:]
  def set_partner(self, partner):
    self.partner = partner
  def send(self,X):
    self.partner.add_to_queue(X)
    self.sends.append(X)
  def receive(self,X):
    val = self.queue.pop(0)
    self.registers[X] = val
    self.receives.append(val)
  def add_to_queue(self, X):
    self.queue.append(X)
    self.is_waiting = False
  def opcode_fn(self, op_type, Z):
    X = Y = None
    if len(Z) == 2:
      X, Y = Z
      try:
        Y = int(Y)
      except:
        Y = self.registers[Y]
    else:
      X = Z[0]
    try: 
      X = int(X)
    except:
      X = X

    self.instruction_pointer += 1
    if op_type == 'snd':
      if type(X) == int:
        self.send(X)
      else:
        self.send(self.registers[X])
    if op_type == 'set':
      self.registers[X] = Y
    if op_type == 'add':
      if type(Y) == int:
        self.registers[X] += Y
      else:
        self.registers[X] += self.registers[Y]
    if op_type == 'mul':
      if type(Y) == int:
        self.registers[X] *= Y
      else:
        self.registers[X] *= self.registers[Y]
    if op_type == 'mod':
      _, self.registers[X] = divmod(self.registers[X], Y)
    if op_type == 'rcv': #always a register index
      #if self.registers[X] == 0:
      #  return
      if len(self.queue) == 0:
        self.is_waiting = True
        self.instruction_pointer -= 1
        return
      self.receive(X)
    if op_type == 'jgz':
      if type(X) == int:
        if X > 0:
          self.instruction_pointer -= 1
          self.instruction_pointer += Y # undo the normal 'next'
      else:
        if self.registers[X] > 0:
          self.instruction_pointer -= 1
          self.instruction_pointer += Y # undo the normal 'next'

  def perform_instruction(self):
    if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.instructions):
      self.is_exited = True
      print('Thread {} is exiting with instruction pointer value = {}'.format(self.id,
      self.instruction_pointer))
      return
    instruct = self.instructions[self.instruction_pointer]
    if instruct[0] == 'rcv' and len(self.queue) == 0:
      # this guy is waiting for his buddy, so we set is_waiting to True and return
      # but definitely do not increment the instruction pointer
      self.is_waiting = True
      return
    #print(instruct, self.instruction_pointer, self.registers, self.queue)
    self.opcode_fn(instruct[0], instruct[1])

def main():
  with open('inputs/day18.txt') as f:
    instructions = [x.strip() for x in f.readlines()]

  instructions = [[x.split()[0], tuple(x.split()[1:])] for x in instructions]
  #registers = defaultdict(int)
  #registers[0] = 0

  thread = Thread(0)
  thread.set_instructions(instructions)
  thread.set_partner(thread) # will this work?

  while not thread.receives:
    thread.perform_instruction()
  print('Part a: the recovered frequency (most recently played sound) is {}'
  .format(thread.sends[-1]))

  thread_0 = Thread(0)
  thread_1 = Thread(1)
  
  thread_0.set_instructions(instructions)
  thread_0.set_partner(thread_1)
  
  thread_1.set_instructions(instructions)
  thread_1.set_partner(thread_0)

  threads = [thread_0, thread_1]
  thread_index = 0
  while True:
    if not thread_0.is_active() and not thread_1.is_active():
      break
    if not threads[thread_index].is_active():
      thread_index = 1 - thread_index
      continue
    threads[thread_index].perform_instruction()

  print('Part b: Program 1 sent a value {} times'.format(len(thread_1.sends)))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

