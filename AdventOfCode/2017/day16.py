import datetime as dt
import re
import string
from collections import deque, defaultdict

def main():
  with open('inputs/day16.txt') as f:
    rounds = f.read().strip().split(',')
  programs = deque(string.ascii_letters[0:16])
  first_round = perform_round(programs, rounds)
  print('Part a: after one round, the program order is {}'.format(''.join(first_round)))
  programs = deque(string.ascii_letters[0:16])
  permutations = defaultdict(int)
  i = 0
  orders = []
  while 2 not in permutations.values():
    programs = perform_round(programs, rounds)
    orders.append(''.join(programs))
    i += 1
    permutations[''.join(programs)] += 1

  #ok we now have a duplicate. Let's find out how long the cycle is
  watch = ''.join(programs)
  cycle_length = 0
  while 1:
    programs = perform_round(programs, rounds)
    orders.append(''.join(programs))
    i += 1
    cycle_length += 1
    if ''.join(programs) == watch:
      break

  _, cycle_index = divmod(1000000000,cycle_length)
  while i%cycle_index > 0:
    programs = perform_round(programs, rounds)
    i += 1
  print('Part b: after 1e9 rounds, the programs order is {}'.format(''.join(programs)))


def perform_round(programs, rounds):
  for r in rounds:
    move(programs, r)
  return programs



def move(p, r):
  if r[0] == 's':
    spin(p, int(r[1:]))
  elif r[0] == 'x':
    i, j = map(int, r[1:].split('/'))
    #i, j = [int(x) for x in r[1:].split('/')]
    exchange(p, j, i)
  elif r[0] == 'p':
    a, b = [x for x in r[1:].split('/')]
    partner(p, a, b)


def spin(p, n):
  p.rotate(n)

def exchange(p, i, j):
  p[i], p[j] = p[j], p[i]

def partner(p, a, b):
  i = p.index(a)
  j = p.index(b)
  p[i], p[j] = p[j], p[i]
  #exchange(p, i, j)

  

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))


