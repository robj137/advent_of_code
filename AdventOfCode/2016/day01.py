import datetime as dt
from collections import defaultdict

class Traveler:
  def __init__(self):
    self.position = 0 + 0j
    self.direction = 0 + 1j
    self.visited = {}
    self.visited_twice = [] 
  def get_position(self):
    return self.position
  def get_distance(self, val):
    return abs(int(val.real)) + abs(int(val.imag))
  def get_current_distance(self):
    return self.get_distance(self.position)
  def travel(self, instruction):
    if instruction[0] == 'L':
      self.direction *= 1j
    else:
      self.direction *= -1j
    distance = int(instruction[1:])
    for x in range(distance):
      self.position += self.direction
      if self.position not in self.visited:
        self.visited[self.position] = 0
      else:
        self.visited_twice.append(self.position)

def main():
  with open('inputs/day1.txt') as f:
    x = f.read()
  directions = [y.strip().strip('\n') for y in x.split(',')]

  traveler = Traveler()
  for d in directions:
    traveler.travel(d)

  pos = traveler.get_position()
  print('Part a: Easter Bunny HQ is {} blocks away'.format(traveler.get_current_distance()))
  print('Part b: on second thought, Easter Bunny HQ is really {} blocks away'.format(traveler.get_distance(traveler.visited_twice[0])))
if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
