import numpy as np
import datetime as dt

def get_uncompressed_length_a(compressed):

  uncompressed = ''
  while compressed:
    if compressed[0] != '(':
      uncompressed += compressed[0]
      compressed = compressed[1:]
    else:
      # this is an open parenthesis that opens up a marker
      next_parenthesis = compressed.find(')')
      marker = compressed[0:next_parenthesis+1].strip(')').strip('(')
      compressed = compressed[next_parenthesis+1:]
      length, times = [int(x) for x in marker.split('x')]
      addition = compressed[0:length]
      compressed = compressed[length:]
      uncompressed += addition * times

  return len(uncompressed)

def get_uncompressed_length_c(compressed):
  score = np.ones([len(compressed), ])
  markers = []

  for i, c in enumerate(compressed):
    if c == '(':
      j = i
      while compressed[j] != ')':
        j += 1
      length, times = [int(x) for x in compressed[i:j+1].strip('(').strip(')').split('x')]
      markers.append([i,j])
      score[j+1:j+1+length] *= times

  for i, j in markers:
    score[i:j+1] = 0
  return int(np.sum(score))

def main():
  with open('inputs/day9.txt') as f:
    compressed = f.read().strip()

  #compressed = 'A(2x2)BCD(2x2)EFG'
  #compressed = 'X(8x2)(3x3)ABCY'
  #compressed = '(6x1)(1x3)A'
  #compressed = '(3x3)XYZ'
  #compressed = 'A(1x5)BC'
  #compressed = 'ADVENT'
  #compressed = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
  #compressed = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
  #compressed = 'X(8x2)(3x3)ABCY'

  print('Part a: the length of the uncompressed string using method a is {}'
  .format(get_uncompressed_length_a(compressed)))
  
  print('Part b; the length of the uncompressed string using method b is {}'
  .format(get_uncompressed_length_c(compressed)))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
