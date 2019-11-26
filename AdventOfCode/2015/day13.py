import string
from datetime import datetime as dt
import re
from itertools import permutations

def get_happiness_from_seating(l, happiness_dict):
    happiness = 0
    for i in range(len(l)):
        happiness += happiness_dict[(l[i-1], l[i])]
        happiness += happiness_dict[(l[i], l[i-1])]

    return happiness

def main():
    
    with open('inputs/day13.txt') as f:
        happies = f.readlines()
    pattern = '([A-Z][a-z]+) would ([a-z]+) (\d+) '
    pattern += 'happiness units by sitting next to ([A-Z][a-z]+)'
    
    happiness_dict = {}
    guests = set()
    for happy in happies:
        result = re.findall(pattern, happy)[0]
        key = (result[0], result[3])
        guests.add(result[0])
        guests.add(result[3])
        adjustment = int(result[2]) * (-1 if result[1] == 'lose' else 1)
        happiness_dict[key] = adjustment

    guests = list(guests)

    happiness_lookup = {}
    for seating in permutations(guests):
        happiness_lookup[tuple(seating)] = get_happiness_from_seating(seating, happiness_dict)

    key_max = max(happiness_lookup.keys(), key=(lambda k: happiness_lookup[k]))
    print(key_max, happiness_lookup[key_max])
    print('Part 1: Total chagne of happiness = {}'.format(happiness_lookup[key_max]))

    for guest in guests:
        happiness_dict[('Me', guest)] = 0
        happiness_dict[(guest, 'Me')] = 0
    
    guests.append('Me')
    happiness_lookup = {}
    for seating in permutations(guests):
        happiness_lookup[tuple(seating)] = get_happiness_from_seating(seating, happiness_dict)
    
    key_max = max(happiness_lookup.keys(), key=(lambda k: happiness_lookup[k]))
    print(key_max, happiness_lookup[key_max])
    print('Part 2: Total change of happiness including me = {}'.format(happiness_lookup[key_max]))

if __name__ == '__main__':
  begin = dt.now()
  main()
  diff_time = dt.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
