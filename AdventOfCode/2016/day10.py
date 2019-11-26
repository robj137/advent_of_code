import datetime as dt
import re
from collections import defaultdict

def main():
  pattern = 'bot (\d+)'
  bots = defaultdict(dict)
  with open('inputs/day10.txt') as f:
    instructions = [x.strip() for x in f.readlines()]
    for i in instructions:
      bots_found = re.findall(pattern, i)
      for bot in bots_found:
        bots[int(bot)] = {  'give_hi_type':None, 
                            'give_lo_type':None, 
                            'hi_val':None, 
                            'lo_val':None,
                            'possess':[], 
                            'compared':[] }

  p1 = 'bot (\d+) gives low to ([a-z]+) (\d+) and high to ([a-z]+) (\d+)'
  p2 = 'value (\d+) goes to bot (\d+)'
  for line in instructions:
    r1 = re.search(p1, line)
    r2 = re.search(p2, line)
    if r1:
      bot, type_lo, b_lo, type_hi, b_hi = r1.groups()
      bot, b_lo, b_hi = [int(x) for x in [bot, b_lo, b_hi]]
      if type_lo == 'output':
        bots[bot]['give_lo_type'] = 'output'
      else:
        bots[bot]['give_lo_type'] = 'bot'
      bots[bot]['lo_val'] = b_lo
      if type_hi == 'output':
        bots[bot]['give_hi_type'] = 'output'
      else:
        bots[bot]['give_hi_type'] = 'bot'
      bots[bot]['hi_val'] = b_hi
    if r2:
      val, bot = [int(x) for x in r2.groups()]
      bots[bot]['possess'].append(val)

  chip_numbers = []
  for b in bots:
    bot = bots[b]
    chip_numbers.extend(bot['possess'])
  chip_numbers.sort()
  part_a(bots, chip_numbers)

def part_a(bots, chip_numbers):
  finished_chip_numbers = []
  output = {}
  while len(output) != len(chip_numbers):
    for b in bots:
      bot = bots[b]
      if len(bot['possess']) == 2:
        bot['possess'].sort()
        bot['compared'] = bot['possess'][:]
        if bot['give_hi_type'] == 'output':
         output[bot['hi_val']] = bot['possess'].pop()
        else:
          bots[bot['hi_val']]['possess'].append(bot['possess'].pop())
        if bot['give_lo_type'] == 'output':
         output[bot['lo_val']] = bot['possess'].pop()
        else:
          bots[bot['lo_val']]['possess'].append(bot['possess'].pop())

  for bot in bots:
    if bots[bot]['compared'] == [17,61]:
      print('Part a: The bot that compared 16 and 61 is {}'.format(bot))

  print('part b: THe value of the product of outputs 0, 1, and 2 is {}'
    .format(output[0]*output[1]*output[2]))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
