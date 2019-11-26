import datetime as dt
import re

def main():
  with open('inputs/day15.txt') as f:
    vals = {g[0]: int(g[1]) for g in [re.search('Generator ([A-Z]+) starts with ([0-9]+)',x.strip()).groups() for x in f.readlines()]}
  
  # for testing
  #vals['A'] = 65
  #vals['B'] = 8921

  factors = {}
  factors['A'] = 16807
  factors['B'] = 48271
  weird = 2147483647
  
  valuesA_A = []
  valuesB_A = []
  valuesA_B = []
  valuesB_B = []

  vA = vals['A']
  vB = vals['B']
  fA = 16807
  fB = 48271
  
  n_matches = 0
  while len(valuesA_B) < 5e6:
    vA = (vA * fA)%weird
    valuesA_A.append(vA)
    if vA % 4 == 0:
      valuesA_B.append(vA)
  
  while len(valuesB_B) < 5e6:
    vB = (vB * fB)%weird
    valuesB_A.append(vB)
    if vB % 8 == 0:
      valuesB_B.append(vB)

  while len(valuesA_A) < 40e6:
    vA = (vA * fA)%weird
    valuesA_A.append(vA)

  while len(valuesB_A) < 40e6:
    vB = (vB * fB)%weird
    valuesB_A.append(vB)

  n_matches_A = 0
  n_matches_B = 0

  for i in range(int(40e6)):
    if valuesA_A[i]%65536 == valuesB_A[i]%65536:
      n_matches_A += 1


  for i in range(int(5e6)):
    if valuesA_B[i]%65536 == valuesB_B[i]%65536:
      n_matches_B += 1

  print('Part A: found {} matches'.format(n_matches_A))
  print('Part B: found {} matches'.format(n_matches_B))

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

