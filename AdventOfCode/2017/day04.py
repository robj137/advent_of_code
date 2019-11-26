import datetime as dt
from collections import Counter

def main():
  passphrases = []
  with open('inputs/day4.txt') as f:
    for line in f:
      passphrases.append([x.strip() for x in line.strip().split()])

  valid = 0
  for passphrase in passphrases:
    c = Counter(passphrase)
    if max(c.values()) == 1:
      valid += 1

  print('Part a: Found {} valid passphrases'.format(valid))

  valid = 0
  for passphrase in passphrases:
    test_phrase = [''.join(sorted(x)) for x in passphrase]
    c = Counter(test_phrase)
    if max(c.values()) == 1:
      valid += 1

  print('Part b: Found {} valid passphrases'.format(valid))

if __name__ == '__main__':     
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

