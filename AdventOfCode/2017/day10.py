import datetime as dt
from collections import deque

def run_round(numbers, lengths, current_position, skip_size):
  n_rotations = current_position
  numbers.rotate(-n_rotations)
  for length in lengths:
    reverse(numbers, length)
    numbers.rotate(-length - skip_size)
    n_rotations += length + skip_size
    skip_size += 1

  current_position = n_rotations%len(numbers)
  numbers.rotate(n_rotations)
  return current_position, skip_size

def main():

  with open('inputs/day10.txt') as f:
    input_line = f.readline().strip()
    lengths_a = [int(x) for x in input_line.split(',')]
    lengths_b = [ord(x) for x in input_line]

  # testing part b
  #lengths_b = [ord(x) for x in 'AoC 2017']
  
  
  
  lengths_b.extend([17, 31, 73, 47, 23])
  
  # Part A
  
  ### test
  #numbers = deque([0, 1, 2, 3, 4])
  #lengths_a = [3, 4, 1, 5]
  ### test
  
  numbers = deque([x for x in range(256)])
  current_position = 0
  skip_size = 0
  run_round(numbers, lengths_a, current_position, skip_size)
  #print(numbers)
  print('Part a: the first product of the first two numbers ({} and {}) is {}'
        .format(numbers[0], numbers[1], numbers[0]*numbers[1]))

  
  #Part B

  numbers = deque([x for x in range(256)])
  current_position = 0
  skip_size = 0
  #print(lengths_b) 
  for _ in range(64):
    current_position, skip_size = run_round(numbers, lengths_b, current_position, skip_size)
  
  dense_hash = convert_sparse_to_dense(numbers)
  print('Part b: the dense hash is {}'.format(dense_hash))

def convert_sparse_to_dense(numbers):
  numbers = list(numbers)
  dense_hash = ''
  while numbers:
    block = numbers[0:16]
    numbers = numbers[16:]
    current = 0
    for number in block:
      current = current ^ number
    dense_hash+=('{0:#0{1}x}'.format(current,2)[-2:])
  return dense_hash

def reverse(l, n):
  # assumes start at 0
  for i in range(int(n/2)):
    l[i], l[n-i-1] = l[n-i-1], l[i]

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

