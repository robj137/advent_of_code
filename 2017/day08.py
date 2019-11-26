import datetime as dt
import re
import numpy as np
from collections import defaultdict, Counter
import operator

label_dict = defaultdict(int)
register_dict = {}

op_dict = {}
op_dict['<'] = operator.lt
op_dict['>'] = operator.gt
op_dict['>='] = operator.ge
op_dict['<='] = operator.le
op_dict['=='] = operator.eq
op_dict['!='] = operator.ne

def main():
  registers = []
  pattern = '([a-z]+) ([a-z]+) (\-*)(\d+) if ([a-z]+) ([!<>=]+) (\-*)(\d+)'
  with open('inputs/day8.txt') as f:
  #with open('inputs/day8.test.txt') as f:
    for line in f:
      registers.append(re.search(pattern, line.strip()).groups())

  ops = []
  for i, reg in enumerate(registers):
    label = reg[0]
    mod = int(reg[2] + reg[3]) * (-1 if reg[1] == 'dec' else 1)
    req_label = reg[4]
    req_cutoff = int(reg[6] + reg[7])
    req_op = reg[5]
    ops.append(reg[5])
    register_dict[i] = {'label':label, 
                            'offset':mod, 
                            'req_label':req_label, 
                            'req_op':req_op,
                            'req_cutoff':req_cutoff}
    label_dict[label] = 0
    label_dict[req_label] = 0

  max_value = 0
  for i in sorted(register_dict.keys()):
    entry = register_dict[i]
    req_value = label_dict[entry['req_label']]
    cutoff = entry['req_cutoff']
    if op_dict[entry['req_op']](req_value, cutoff):
      label_dict[entry['label']] += entry['offset']
    max_value = max(max_value, max(label_dict.values()))
  print('Part a: Largest value in any register at end of operations is {}'.format(max(label_dict.values())))
  print('Part b: Largest value in any register for lifetime of operations is {}.'.format(max_value))


if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

