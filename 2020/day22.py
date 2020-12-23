import datetime as dt
from collections import Counter, defaultdict, deque
from datetime import datetime as dt
import numpy as np
import re
from copy import deepcopy


def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day22.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day22.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]

    current_player = 'Player 1'
    decks = {}
    decks['Player 1'] = []
    decks['Player 2'] = []

    for line in lines:
        if 'Player' in line:
            current_player = line.split(':')[0]
        elif len(line) > 0:
            decks[current_player].append(int(line))

    return decks

def run(decks, use_recursion=0):
    #print("starting at level", use_recursion, decks)
    time = dt.now()
    snapshots = {}
    p1 = decks['Player 1']
    p2 = decks['Player 2']
    while len(p1) > 0 and len(p2) > 0:
        #print(time, decks)
        recursiveable = False
        snapshot = str(decks)
        if snapshot in snapshots:
            return 'Player 1', decks
        else:
            snapshots[snapshot] = 1
        s1 = p1[0]   
        s2 = p2[0]
        if len(p1) - 1 >= s1 and len(p2) - 1 >= s2:
            recursiveable = True
        if use_recursion and recursiveable:
            p1.rotate(-1)
            p2.rotate(-1)
            s1 = p1.pop()
            s2 = p2.pop()
            new_deck = deepcopy(decks)
            new_p1 = new_deck['Player 1']
            new_p2 = new_deck['Player 2']
            while len(new_p1) > s1:
                new_p1.pop()
            while len(new_p2) > s2:
                new_p2.pop()
            winner, _ = run(new_deck, use_recursion)
            if winner == 'Player 1':
                p1.append(s1)
                p1.append(s2)
            else:
                p2.append(s2)
                p2.append(s1)
            

        else:
            
            p1.rotate(-1)
            p2.rotate(-1)
            if s2 > s1:
                p2.append(p1.pop())
            else:
                p1.append(p2.pop())

    winner = 'Player 1' if len(p1) > 0 else 'Player 2'
    return winner, decks
    
    winner = decks['Player 1'] if len(decks['Player 1']) > 0 else decks['Player 2']
    print(decks)
    print(winner)
    winner.reverse()
    score = 0
    for i, x in enumerate(winner):
        score += (i+1) * x

    print('score is', score)

def score_deck(decks):
    score = 0
    print('scoring decks', decks)
    for player in decks:
        deck = decks[player]
        deck.reverse()
        for i, x in enumerate(deck):
            score += (i+1) * x
    return score

if __name__ == '__main__':
    begin = dt.now()
    is_test = False
    decks = get_data(is_test)
    for x in decks:
        decks[x] = deque(decks[x])
    print(decks)
    winner, decks = run(decks)
    print(score_deck(decks))
    decks = get_data(is_test)
    for x in decks:
        decks[x] = deque(decks[x])
    winner, decks = run(decks, True)
    print(score_deck(decks))
    #part_1_answer = run(rules, messages)
    #part_1_time = dt.now()
    #diff_time = dt.now() - begin
    #print('Part 1: {}'.format(part_1_answer))
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #rules, messages = get_data(is_test, part2=True)
    #part_2_answer = run(rules, messages)
    #diff_time = dt.now() - part_1_time
    #print('Part 12 {}'.format(part_2_answer))
    
   # print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
