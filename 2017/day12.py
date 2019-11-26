import datetime as dt
from collections import defaultdict
import numpy as np


def main():
  program_graph = defaultdict(list)
  lines = []
  with open('inputs/day12.txt') as f:
    for line in f:
      p1 = int(line.split('<->')[0])
      program_graph[p1].extend([int(x) for x in line.split('<->')[1].split(',')])

  groups = []

  while program_graph:
    connections = []
    find_connections(sorted(program_graph.keys())[0], program_graph, connections)
    groups.append(connections[:])
    for key in connections:
      del program_graph[key]

  for g in groups:
    if 0 in g:
      print('Part a: the Zero group has {} connections'.format(len(g)))

  print('Part b: There are {} groups in total'.format(len(groups)))

def find_connections(program, graph, zero_list):
  # recursion time again!
  # want to look at connections.
  for p in graph[program]:
    if p not in zero_list:
      zero_list.append(p)
      find_connections(p, graph, zero_list)
  return


if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

