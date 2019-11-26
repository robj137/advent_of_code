import datetime as dt
import re
from collections import Counter, deque
import string

def calculate_checksum(s):
  s = s.replace('-', '')
  c = Counter(s)
  return ''.join(sorted(list(c.keys()), key=lambda x: (-c[x], x))[0:5])

def get_real_name(room_name, sector_id):
  name = ''
  d = deque(string.ascii_lowercase)
  for c in room_name:
    if c == '-':
      name += ' '
    else:
      d.rotate(-1 * d.index(c))
      d.rotate(-1 * sector_id)
      name += d[0]
  return name

def main():
  pattern = '([a-z-]+)-(\d+)\[([a-z]+)\]'
  rooms = {}
  with open('inputs/day4.txt') as f:
    for line in f:
      info = re.search(pattern, line.strip()).groups()
      name = info[0]
      rooms[name] = {'sector_id': int(info[1]), 
                      'given_checksum': info[2], 
                      'calculated_checksum':calculate_checksum(name)}
      rooms[name]['is_decoy'] = rooms[name]['given_checksum'] != rooms[name]['calculated_checksum']
      rooms[name]['real_name'] = get_real_name(name, int(info[1]))
  
  sum_of_sector_ids = 0
  for room in rooms:
    if not rooms[room]['is_decoy']:
      sum_of_sector_ids += rooms[room]['sector_id']

  print('Part a: sum of sector ids for real rooms is {}'.format(sum_of_sector_ids))

  for room in rooms:
    if 'north' in rooms[room]['real_name']:
      print('Part b: the sector id of the room for {} is {}'
      .format(rooms[room]['real_name'], rooms[room]['sector_id']))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
