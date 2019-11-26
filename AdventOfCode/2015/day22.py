import sys
import re
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
import json

def get_boss_stats(test=False):
    d = {
        'Hit Points': 51,
        'Damage': 9
    }
    if test:
        d['Hit Points'] = 14
        d['Damage'] = 8
    return d

def get_player_stats(test=False, part_2 = False):
    d = {
            'Hit Points': 50,
            'Mana': 500,
            'TotalManaSpent': 0,
            'HardMode': part_2
        }
    if test:
        d['Hit Points'] = 10
        d['Mana'] = 250
    return d

class Encounter:
    """We are exploring all spell options. A new encounter is spawned
       whenever the player chooses a new spell. So the encounter actually
       starts midway through the player's turn (after effects have taken
       effect)."""
    
    # The encounter is of course controlled by the arena. The arena progreses
    # with the rest of the player's turn (checks for death of both), then performs
    # the bosses turn (and checks for death for both), and then the beginning of the
    # player's next turn (effects), and checks for death, and then spawns a NEW
    # encounter for any possible 
    
    def __init__(self, spell, boss_stats, player_stats, effects):
        # create new boss and player, new copies of everything in memory
        self.boss = Boss(boss_stats)
        self.player = Player(player_stats)
        self.effects = effects.copy()
        self.spell = spell

    def get_spell(self):
        return self.spell
    def get_player(self):
        return self.player
    def get_boss(self):
        return self.boss
    def get_effect_counter(self):
        return self.effects


class Arena:
    def __init__(self, boss, player):
        # Initial boss and player stats
        
        # the player, boss,and effect counter will get reloaded again and again
        self.player = player
        self.boss = boss
        self.effect_counter = {
                                'Shield': 0,
                                'Poison': 0,
                                'Recharge': 0,
                                'Magic Missile': 0,
                                'Drain': 0
                            }
        
        self.spell_ledger = {
                                'Magic Missile': 53,
                                'Drain': 73,
                                'Shield': 113,
                                'Poison': 173,
                                'Recharge': 229
                            }

        # rather than strictly 'turn-based', it's encounter based (lifo)
        self.encounter_queue = []
        
        # we also want to keep track of games (won and lost)
        self.results = defaultdict(list)

        # finally, to not reprocess, keep track of what's already been done
        self.already_processed = {}

    def iterate_effects(self):
        if self.effect_counter['Shield'] > 0:
            self.player.set_defense(7)
            self.effect_counter['Shield'] -= 1
        else:
            self.player.set_defense(0)
        
        if self.effect_counter['Poison'] > 0:
            self.boss.take_damage(3)
            self.effect_counter['Poison'] -= 1
        
        if self.effect_counter['Recharge'] > 0:
            self.player.add_mana(101)
            self.effect_counter['Recharge'] -= 1

    def check_for_winner(self):
        if not self.boss.is_alive:
            self.results['Player'].append(self.player.total_mana_spent)
            return 'Player'
        if not self.player.is_alive:
            self.results['Boss'].append(self.player.total_mana_spent)
            return 'Boss'
        return None
   
    def get_string_rep(self, objs):
        return json.dumps(objs)

    def run_encounter(self, encounter):
        # load the encounter details
        self.player = encounter.get_player()
        self.boss = encounter.get_boss()
        self.effect_counter = encounter.get_effect_counter()
        spell = encounter.get_spell()

        
        self.cast_spell(spell)
        if self.check_for_winner():
            return
        
        # now the boss's turn

        self.iterate_effects()
        if self.check_for_winner():
            return
        
        self.player.take_damage(self.boss.damage)
        if self.check_for_winner():
            return

        # still alive, eh? beginning of player's turn, so iterate effects
        # and choose a spell to cast
        if self.player.is_hard_mode:
            self.player.take_damage(1)
        self.iterate_effects()
        if self.check_for_winner():
            return
        
        for spell in self.spell_ledger:
            # enough mana and able to cast spell?
            if self.spell_ledger[spell] < self.player.mana and self.effect_counter[spell] == 0:
                obj_s = json.dumps([spell, self.boss.get_stats(), self.player.get_stats(), self.effect_counter])
                if obj_s in self.already_processed:
                    return
                self.already_processed[obj_s] = 0
                encounter = Encounter(spell, self.boss.get_stats(), self.player.get_stats(), self.effect_counter)
                self.encounter_queue.append(encounter)

        # all done here

    def cast_spell(self, spell):
        if spell == 'Magic Missile':
            self.player.spend_mana(53)
            self.boss.take_damage(4)
        if spell == 'Drain':
            self.player.spend_mana(73)
            self.player.hp += 2
            self.boss.take_damage(2)
        if spell == 'Shield':
            self.player.spend_mana(113)
            self.effect_counter['Shield'] = 6
        if spell == 'Poison':
            self.player.spend_mana(173)
            self.effect_counter['Poison'] = 6
        if spell == 'Recharge':
            self.player.spend_mana(229)
            self.effect_counter['Recharge'] = 5
    
    
    def fight(self):
        # bootstrap our way to an encounter by playing half of first round
        if self.player.is_hard_mode:
            self.player.take_damage(1)
        self.iterate_effects()
        if self.check_for_winner():
            return
        for spell in self.spell_ledger:
            # enough mana and able to cast spell?
            if self.spell_ledger[spell] < self.player.mana and self.effect_counter[spell] == 0:
                encounter = Encounter(spell, self.boss.get_stats(), self.player.get_stats(), self.effect_counter)
                self.encounter_queue.append(encounter)

        while self.encounter_queue:
            self.run_encounter(self.encounter_queue.pop())

        # after all is said and done, should have a list of 

class Boss:
    def __init__(self, stats):
        self.hp = stats['Hit Points']
        self.damage = stats['Damage']
        self.defense = 0
        self.is_alive = True

    def take_damage(self, external_damage):
        self.hp -= max(1, external_damage - self.defense)
        if self.hp <= 0:
            self.is_alive = False

    def get_stats(self):
        stats = {
                    'Hit Points': self.hp,
                    'Damage': self.damage
                }
        return stats

class Player:
    def __init__(self, stats):
        self.hp = stats['Hit Points']
        self.mana = stats['Mana']
        self.total_mana_spent = stats['TotalManaSpent']
        self.is_hard_mode = stats['HardMode']
        self.defense = 0
        self.is_alive = True

    def get_stats(self):
        stats = {
                    'Hit Points': self.hp,
                    'Mana': self.mana,
                    'TotalManaSpent': self.total_mana_spent,
                    'HardMode': self.is_hard_mode
                }
        return stats

    def take_damage(self, external_damage):
        self.hp -= max(1, external_damage - self.defense)
        if self.hp <= 0:
            self.is_alive = False

    def spend_mana(self, mana):
        self.mana -= mana
        self.total_mana_spent += mana
    def add_mana(self, mana):
        self.mana += mana
    def set_defense(self, defense):
        self.defense = defense
    def get_damage(self):
        return self.damage
    def get_defense(self):
        return self.defense
    def get_hp(self):
        return self.hp

def part1():
    test = False
    player = Player(get_player_stats(test))
    boss = Boss(get_boss_stats(test))

    arena = Arena(boss, player)
    arena.fight()


    min_mana_win = min(arena.results['Player'])
    max_mana_lose = max(arena.results['Boss'])

    print('Part 1: Least amount of mana spent to win is {}'.format(min_mana_win))

def part2():
    test = False
    player = Player(get_player_stats(test, True))
    boss = Boss(get_boss_stats(test))

    arena = Arena(boss, player)
    arena.fight()


    min_mana_win = min(arena.results['Player'])
    max_mana_lose = max(arena.results['Boss'])
    print('Part 2: Least amount of mana spent to win is {} (on hard mode)'.format(min_mana_win))

def main():
    part1()
    part2()


if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
