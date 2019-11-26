import pandas as pd
import numpy as np
import datetime as dt
import re

class SurgeonGeneral:
  def __init__(self):
    self.all_groups = []
    self.immune_system_army = []
    self.infection_army = []
    self.infection_army_count = 0
    self.immune_system_army_count = 0

  def is_winner(self):
    if self.infection_army_count > 0 and self.immune_system_army_count > 0:
      return False
    return True

  def add_boost(self, affiliation, boost):
    boosted_army = self.immune_system_army
    if affiliation == 'Infection':
      boosted_army = self.infection_army_count
    for g in boosted_army:
      g.attack_power += boost
  def add_group(self, affiliation, group):
    self.all_groups.append(group)
    if affiliation == 'Immune System':
      self.immune_system_army.append(group)
      self.immune_system_army_count += group.number
    else:
      self.infection_army.append(group)
      self.infection_army_count += group.number

  def perform_round_maintenance(self):
    for group in self.all_groups:
      group.effective_power = group.number * group.attack_power
      group.in_play = (group.effective_power > 0)
      group.current_target = None
    self.all_groups.sort(key=lambda x: x.effective_power + 0.001*x.initiative, reverse=True)
    self.infection_army_count = 0
    self.immune_system_army_count = 0
    for g in self.immune_system_army:
      self.immune_system_army_count += g.number
    for g in self.infection_army:
      self.infection_army_count += g.number
  def get_available_groups(self, affiliation):
    available = []
    if affiliation == 'Immune System':
      side = self.immune_system_army
    else:
      side= self.infection_army
    for g in side:
      if g.in_play:
        available.append(g)
    return available

  def select_targets(self):
    targets = {}
    targets['Infection'] = self.get_available_groups('Immune System')
    targets['Immune System'] = self.get_available_groups('Infection')
    for group in self.all_groups:
      # for this group, need to calculate how much damage it would do against all opposing
      # (available) groups
      damage_scores = []
      for target in targets[group.affiliation]:
        damage_scores.append(self.get_damage_score(group, target, True))
      if damage_scores:
        if max(damage_scores) > 0:
          group.current_target = targets[group.affiliation].pop(np.argmax(damage_scores)) 
    # round maintenance already performed, so all_groups is already grouped by effective power
  
  def get_damage_score(self, group, target, tie_breaker=False):
    if not target:
      return 0
    attack_type = group.attack_type
    multiplier = 1
    
    if attack_type in target.weakness:
      multiplier *= 2
    if attack_type in target.immunity:
      multiplier *= 0
    return multiplier * (group.effective_power + tie_breaker*(1e-6 * target.effective_power  + 1e-9 * target.initiative))

  def attack_phase(self):
    # now to sort by initiative
    self.all_groups.sort(key=lambda x: x.initiative, reverse=True)
    for group in self.all_groups:
      self.perform_attack(group)
  
  def perform_attack(self, group):
    if not group.in_play:
      #oops, this group has no more members, so nothing to do
      return
    if not group.current_target:
      #nothing to attack this round
      return
    target = group.current_target
    damage = self.get_damage_score(group, target, False)
    units_killed = int(damage/target.hp)
    #print('attacker power: {}, attacker number: {}, effective power 1: {}, effective power 2: {}'
    #.format(group.attack_power, group.number, group.effective_power, group.attack_power * group.number))
    #print(damage, target.number, target.hp, units_killed)
    target.number -= units_killed
    target.effective_power = target.number * target.attack_power
    if target.number < 1:
      target.number = 0
      target.in_play = False

class Group:
  def __init__(self, affiliation, group_line):
    self.affiliation = affiliation
    number, hp, attack_power, attack_type, initiative, weakness, immunity = self.parse_group_line(group_line)
    self.number = int(number)
    self.hp = int(hp)
    self.attack_power = int(attack_power)
    self.attack_type = attack_type
    self.initiative = int(initiative)
    self.weakness = weakness
    self.immunity = immunity
    self.effective_power = self.number * self.attack_power
    self.in_play = True
    self.current_target = None

  def parse_group_line(self, line):
    pattern = '(\d+) units each with (\d+) hit points (.*)with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)'
    n, hp, immunity_weakness, attack_power, attack_type, initiative = re.search(pattern, line).groups()
    weakness, immunity = self.parse_weakness_immunities(immunity_weakness)
    return n, hp, attack_power, attack_type, initiative, weakness, immunity
    
  def parse_weakness_immunities(self, blurb):
    weakness = []
    immunity = []
    w_i = [weakness, immunity]
    blurb = [x.strip().strip(')').strip('(') for x in blurb.split(';')]
    for b in blurb:
      if len(b) > 0:
        #print('__', len(b), b)
        if b.split(' ')[0] == 'weak':
          value_bin = 0
        else:
          value_bin = 1
        values = b.split('to ')[1].split(',')
        w_i[value_bin].extend([x.strip() for x in values])
    return weakness, immunity

def set_up_arena():
  belligerents = []
  sg = SurgeonGeneral()
  in_file = 'inputs/day24.txt'
  with open(in_file) as f:
    lines = [x.strip() for x in f.readlines()]
  affiliation = ''
  for line in lines:
    if ':' in line:
      affiliation = line.split(':')[0]
    if 'units' in line:
      group = Group(affiliation, line)
      sg.add_group(affiliation, group)
  
  return sg

def campaign(boost=0):
  sg = set_up_arena()
  sg.add_boost('Immune System', boost)
  sg.perform_round_maintenance()
  prev_immune = 0
  prev_infection = 0
  while not sg.is_winner():
    sg.select_targets()
    sg.attack_phase()
    sg.perform_round_maintenance()
    if prev_immune == sg.immune_system_army_count and prev_infection == sg.infection_army_count:
      # it's a tie, return 0 
      return 0
    prev_immune = sg.immune_system_army_count
    prev_infection = sg.infection_army_count
    #print('Int. result:', [(x.number) for x in sg.immune_system_army],
    #[(x.number) for x in sg.infection_army])
  
  return (sg.immune_system_army_count - sg.infection_army_count)

def main():
  print ('Part a: the number of remaining units is {}'.format(np.abs(campaign(0))))
  i = 0
  while 1:
    i += 1
    counts = campaign(i)
    if counts > 0:
      print('Part b: the number of remaining units with a boost of {} is {}'.format(i, counts))
      break

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
