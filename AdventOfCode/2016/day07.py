import datetime as dt
import re

def is_abba(s):
  for i in range(len(s)-3):
    trial = s[i:i+4]
    if trial[0] == trial[3] and trial[1] == trial[2] and trial[0] != trial[1]:
      return True
  return False

def get_aba(s):
  aba = []
  for i in range(len(s)-2):
    trial = s[i:i+3]
    if trial[0] == trial[2] and trial[0] != trial[1]:
      aba.append(trial)
  return aba

def aba_to_bab(abas):
  babs = []
  # will return a list
  if type(abas) != list:
    abas = [abas]
  for x in abas:
    babs.append(x[1:] + x[1])
  return babs

def is_aba_and_bab(hypernet, supernet):
  abas = []
  for s in supernet:
    abas.extend(get_aba(s))
  babs = []
  for s in hypernet:
    babs.extend(get_aba(s))
  babs = aba_to_bab(babs)
  return not set(abas).isdisjoint(babs)

def main():
  ips = {}
  pattern = '\[([a-z]+)\]'
  with open('inputs/day7.txt') as f:
    for line in f:
      hypernet_sequences = re.findall(pattern, line.strip())
      remainder = line
      for s in hypernet_sequences:
        remainder = remainder.strip().replace(s, ' ')
      supernet_sequences = [x.strip('[').strip(']') for x in remainder.split()]
      ips[line.strip()] = {'ip':line.strip(), 'hypernet':hypernet_sequences, 'supernet':supernet_sequences}
      supports_TLS = False
      for x in supernet_sequences:
        if is_abba(x):
          supports_TLS = True
      for x in hypernet_sequences:
        if is_abba(x):
          supports_TLS = False
      ips[line.strip()]['supports_TLS'] = supports_TLS
      ips[line.strip()]['supports_SSL'] = is_aba_and_bab(hypernet_sequences, supernet_sequences)

  n_TLS = 0
  n_SSL = 0
  for ip in ips:
    if ips[ip]['supports_TLS']:
      n_TLS+=1
    if ips[ip]['supports_SSL']:
      n_SSL+=1

  print('Part a: Found {} IP addresses that support TLS'.format(n_TLS))
  print('Part a: Found {} IP addresses that support SSL'.format(n_SSL))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
