import sys
import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict

def get_boss_stats(test=False):
    d = {
        'Hit Points': 104,
        'Damage': 8,
        'Armor': 1
    }
    if test:
        d['Hit Points'] = 12
        d['Damage'] = 7
        d['Armor'] = 2
    return d

class Arena:
    def __init__(self, boss_stats, player):
        self.boss_hp = boss_stats['Hit Points']
        self.boss_damage = boss_stats['Damage']
        self.boss_defense = boss_stats['Armor']
        self.boss_is_alive = True

        self.player = player

        self.winner = None

    def damage_boss(self, external_damage):
        self.boss_hp -= max(1, external_damage - self.boss_defense)
        if self.boss_hp <= 0:
            self.boss_is_alive = False

    def get_gold_spent(self):
        return self.player.get_gold_spent()

    def take_turn(self):
        # player goes first
        self.damage_boss(self.player.get_damage())
        if not self.boss_is_alive:
            self.winner = 'Player'
            return
        self.player.take_damage(self.boss_damage)


    def fight(self):
        if not self.player.is_alive:
            # forfeit
            return 'Forfeit'
        while not self.winner:
            self.take_turn()
            if not self.boss_is_alive:
                self.winner = 'Player'
            if not self.player.is_alive:
                self.winner = 'Boss'
        return self.winner

class Player:
    def __init__(self, weapon, armor, ring1, ring2):
        self.is_alive = True
        self.weapon = weapon
        self.armor = armor
        self.ring1 = ring1
        self.ring2 = ring2
        self.hp = 100
        self.gold_spent = 0
        self.calculate_damage()
        self.calculate_defense()
        if ring1 == ring2 and ring1:
            self.is_alive = False
            # rather than deal with combinatorics, just fail the player
            self.damage = 0
            self.hp = 0
            self.defense = 0

    def calculate_damage(self):
        self.damage = 0
        if self.weapon == 'Dagger':
            self.damage += 4
            self.gold_spent += 8
        elif self.weapon == 'Shortsword':
            self.damage += 5
            self.gold_spent += 10
        elif self.weapon == 'Warhammer':
            self.damage += 6
            self.gold_spent += 25
        elif self.weapon == 'Longsword':
            self.damage += 7
            self.gold_spent += 40
        elif self.weapon == 'Greataxe':
            self.damage += 8
            self.gold_spent += 74
        else:
            print('need to choose a valid weapon!')
            sys.exit()

        for ring in [self.ring1, self.ring2]:
            if ring and 'Damage' in ring:
                extra_damage = int(ring.split('+')[1])
                self.damage += extra_damage
                self.gold_spent += [25, 50, 100][extra_damage-1]

    def calculate_defense(self):
        self.defense = 0
        if self.armor == 'Leather':
            self.defense += 1
            self.gold_spent += 13
        elif self.armor == 'Chainmail':
            self.defense += 2
            self.gold_spent += 31
        elif self.armor == 'Splintmail':
            self.defense += 3
            self.gold_spent += 53
        elif self.armor == 'Bandedmail':
            self.defense += 4
            self.gold_spent += 75
        elif self.armor == 'Platemail':
            self.defense += 5
            self.gold_spent += 102

        for ring in [self.ring1, self.ring2]:
            if ring and 'Defense' in ring:
                extra_defense = int(ring.split('+')[1])
                self.defense += extra_defense
                self.gold_spent += [20, 40, 80][extra_defense-1]

    def get_gold_spent(self):
        return self.gold_spent
     
    def take_damage(self, external_damage):
        self.hp -= max(1, external_damage - self.defense)
        if self.hp <= 0:
            self.is_alive = False

    def get_damage(self):
        return self.damage
    def get_defense(self):
        return self.defense
    def get_hp(self):
        return self.hp


def main():
    weapons = ['Dagger', 'Shortsword', 'Warhammer', 'Longsword', 'Greataxe']
    armors = [None, 'Leather', 'Chainmail', 'Splintmail', 'Bandedmail', 'Platemail']
    rings = [None, 'Damage +1', 'Damage +2', 'Damage +3', 'Defense +1', 'Defense +2', 'Defense +3']
    boss_stats = get_boss_stats()
    winning_campaigns = defaultdict(list)
    losing_campaigns = defaultdict(list)
    n_campaigns = 0
    n_winning_campaigns = 0
    for weapon in weapons:
        for armor in armors:
            for ring1 in rings:
                for ring2 in rings:
                    n_campaigns += 1
                    p = Player(weapon, armor, ring1, ring2)
                    arena = Arena(boss_stats, p)
                    winner = arena.fight()
                    if winner == 'Player':
                        n_winning_campaigns += 1
                        winning_campaigns[arena.get_gold_spent()].append([weapon, armor, ring1, ring2])
                    if winner == 'Boss':
                        losing_campaigns[arena.get_gold_spent()].append([weapon, armor, ring1, ring2])
    print('total of {} campaigns, of which {} were won by player'.format(n_campaigns, n_winning_campaigns))
    min_key = min(winning_campaigns)
    print('Part 1: Least amount of gold spent is {}'.format(min_key))
    print('with the following accroutements: {}'.format(winning_campaigns[min_key]))

    max_key = max(losing_campaigns)
    print('Part 2: Most amont of gold spent to lose is {}'.format(max_key))
    print('with the following accroutements: {}'.format(losing_campaigns[max_key]))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
