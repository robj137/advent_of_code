import pandas as pd
import numpy as np
import datetime as dt
import heapq

class Dungeon:
  def __init__(self, infile):
    lines = []
    with open(infile) as f:
      for line in f:
        lines.append([x for x in line.strip()])
    self.dungeon_map = np.array(lines)
    self.get_dungeon_neighbors()
  
  def print_map(self):
    for line in self.dungeon_map:
      print((''.join(line)).replace('#','█').replace('.', ' '))
  
  def set_belligerents(self, belligerents_list):
    self.belligerents = belligerents_list
    self.belligerents_alive = belligerents_list

  def sort_belligerents(self): # sort the characters by reading list
    self.belligerents = sorted(self.belligerents, key = lambda x: x.get_position()[1]*0.00001 + x.get_position()[0] * 0.01)
  
  def perform_round(self):
    self.sort_belligerents()
    for fighter in self.belligerents:
      fighter.perform_turn()
  
  def get_score(self):
    scores = {'Elf':0, 'Goblin':0}
    for enemy in self.belligerents_alive:
      scores[enemy.type] += enemy.get_hp()

    if scores['Elf'] == 0 or scores['Goblin'] == 0:
      return False, scores['Elf'] - scores['Goblin']
  
    return True, scores['Elf'] - scores['Goblin']
  
  def get_dungeon_neighbors(self):
    dungeon_neighbors = {}
    for p in [np.array([x,y]) for x in range(self.dungeon_map.shape[0]) for y in range(self.dungeon_map.shape[1])]:
      if self.dungeon_map[tuple(p)] != '█':
        dungeon_neighbors[tuple(p)] = []
        for delta in [(0,1), (0,-1), (1,0), (-1,0)]:
          if self.is_open_square(p+delta, True):
            dungeon_neighbors[tuple(p)].append(tuple(p+delta))
    self.dungeon_neighbors = dungeon_neighbors

  def is_open_square(self, p, ignore_fighters):
    for i in [0,1]:
      if p[i] < i or p[i] >= self.dungeon_map.shape[i]:
        return False
    if ignore_fighters:
      return self.dungeon_map[tuple(p)] != '█'
    if self.dungeon_map[tuple(p)] != '.':
      return False
    return True

  def get_live_enemy_from_position(self, friendly_type, pos):
    for enemy in self.belligerents_alive:
      if tuple(enemy.get_position()) == tuple(pos) and enemy.type != friendly_type:
        return enemy
    return None

  def get_heuristic(self, p1, p2):
    # manhattan distance to target from current cell
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


  def path_search(self, p1, p2, forbidden = []):
    p1 = tuple(p1)
    p2 = tuple(p2)
    if p1 == p2:
      return 0,0, [p2], p2
    visited = {}
    notVisited = {}
    for key in self.dungeon_neighbors.keys():
      if key not in forbidden:
        notVisited[key] = self.dungeon_neighbors[key]

    heap = []
    heapq.heappush(heap, [1, 1, p1, [p1] ])
    first_step = False
    while heap:
      _, s, thisVtxKey, path = heapq.heappop(heap)
      if thisVtxKey not in visited:
        visited[thisVtxKey] = notVisited.pop(thisVtxKey)
        for vtx in self.dungeon_neighbors[thisVtxKey]:
          if vtx not in visited and vtx not in forbidden:
            sum1 = s + 1
            heapq.heappush(heap, [sum1 + self.get_heuristic(vtx, p2), sum1,vtx,path + [vtx]])
            if vtx == p2:
              return sum1, sum1, path, vtx
    # well that didn't work, so we return a bunch of 'inf's
    return float('inf'), float('inf'), [(float('inf'), float('inf'))], (float('inf'), float('inf'))
  

class Fighter:
  
  def __init__(self, race, attack_power, hp, pos, enemy_type):
    self.type = race
    self.hp = hp
    self.attack_power = attack_power
    self.position = pos
    self.is_alive = True
    self.enemy_type = enemy_type

  def set_dungeon(self, dungeon):
    self.dungeon = dungeon
  
  def set_position(self, loc):
    self.position = loc
  
  def get_position(self):
    return self.position
  
  def get_hp(self):
    return self.hp
  
  def deal_blow(self, power):
    self.hp -= power
    if self.hp <= 0:
      self.is_alive = False
  
  def get_is_alive(self):
    return self.is_alive
  
  def perform_turn(self):
    if not self.get_is_alive():
      return
    destination = self.identify_targets_and_get_ranges()
    self.move(destination)
    self.attack()
  def identify_targets_and_get_ranges(self):
    forbidden = [tuple(x.position) for x in self.dungeon.belligerents_alive]
    forbidden.pop(forbidden.index(tuple(self.position)))
    targets = np.argwhere(self.dungeon.dungeon_map == self.enemy_type)
    ranges = []
    for target in targets:
      for delta in [(0,1), (0,-1), (1,0), (-1,0)]:
        if tuple(target+delta) == tuple(self.position):
          return self.position
        if self.dungeon.is_open_square(target + delta,  False):
          ranges.append(target+delta)
    if not ranges:
      return self.position
    ranges = np.unique(ranges, axis=0)
    distances = []
    for r in ranges:
      d = self.dungeon.path_search(self.position, r, forbidden)
      length = d[0] + 0.01*r[0] + 0.0001*r[1]
      distances.append(length)
    i = np.argmin(distances)
    return ranges[i]

  def move(self, destination):
    forbidden = [tuple(x.position) for x in self.dungeon.belligerents_alive]
    if tuple(self.position) == tuple(destination): #hooray, we're already there
      return
    weights = [0.3,0.2,0.1,0.0]
    first_steps = [(0,0), (0,0), (0,0), (0,0)]
    for i, delta in enumerate([(1,0), (0,1), (0,-1), (-1,0)]):
      if self.dungeon.is_open_square(np.array(self.get_position()) + delta, False):
        _, weight, path, vts = self.dungeon.path_search(np.array(self.position) + delta, destination, forbidden)
        weights[i] += weight
        if path: 
          first_steps[i] = path[0]
      else:
        weights[i] = float('inf')
    if min(weights) == float('inf'):
      return # now here to go
    self.dungeon.dungeon_map[tuple(self.position)] = '.'
    self.set_position(first_steps[np.argmin(weights)])
    self.dungeon.dungeon_map[tuple(self.position)] = self.type[0]
  def attack(self):
    targets = np.argwhere(self.dungeon.dungeon_map == self.enemy_type)
    target = None
    weights = [300,300,300,300]
    enemies = 4*[None]
    for i, delta in enumerate([(-1,0), (0,-1), (0,1), (1,0)]):
      s = tuple(np.array(self.position) + delta)
      enemy = self.dungeon.get_live_enemy_from_position(self.type, tuple(np.array(self.position) + delta))
      if enemy:
        weights[i] = enemy.get_hp() + i*0.01 #tie breaker
        enemies[i] = enemy
    enemy = enemies[np.argmin(weights)]
    if not enemy:
      return # nothing to attack
    enemy.deal_blow(self.attack_power)
    if not enemy.get_is_alive():
      self.dungeon.belligerents_alive.pop(self.dungeon.belligerents_alive.index(enemy))
      self.dungeon.dungeon_map[tuple(enemy.get_position())] = '.'

def run_campaign(elf_power=3):
  dungeon = Dungeon('inputs/day15.txt')

  elves = np.argwhere(dungeon.dungeon_map == 'E')
  n_elves = len(elves)
  goblins = np.argwhere(dungeon.dungeon_map == 'G')

  belligerents = []
  for elf in elves:
    fighter = Fighter('Elf', elf_power, 200, elf, 'G')
    fighter.set_dungeon(dungeon)
    belligerents.append(fighter)
  for orc in goblins:
    fighter = Fighter('Goblin', 3, 200, orc, 'E')
    fighter.set_dungeon(dungeon)
    belligerents.append(fighter)

  dungeon.set_belligerents(belligerents)

  dungeon.print_map()
  keep_going, score_differential = dungeon.get_score()
  i = 0
  while keep_going:
    if len(np.argwhere(dungeon.dungeon_map == 'E')) != n_elves:
      print('\noh no!\n')
      return -1
    dungeon.perform_round()
    keep_going, score_differential = dungeon.get_score()
    if not keep_going:
      break
    i += 1
    print('\nElf Power: {}'.format(elf_power))
    print('end of round {}'.format(i+1))
    dungeon.print_map()
  if elf_power == 3:
    print('Part a: THe outcome is {}'.format(score * i))
  print('\n oh yeah! \n')
  dungeon.print_map()
  return score_differential*i

def main():
  keep_going = True
  successes = []
  failures = []
  elf_power = 3
  scores = {}
  while keep_going:
    outcome = run_campaign(elf_power)
    scores[elf_power] = outcome
    if outcome > 0:
      successes.append(elf_power)
    else:
      failures.append(elf_power)
    if not successes:
      elf_power *= 2
    else:
      elf_power = int(max(failures) + 0.5*(min(successes) - max(failures)))
    if successes:
      if min(successes) - 1 in failures:
        keep_going = False
        print('Part b: Outcome with all surviving elves is {}'.format(scores[min(successes)]))
    
if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
