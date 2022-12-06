import numpy as np
import pandas as pd
import sys

def get_data(is_test=True):
    path = 'inputs/day04.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    number_draw = [int(x) for x in lines.pop(0).strip().split(',')]
    
    cards = []
    while lines and lines[0] == '\n':
        lines.pop(0)
        cards.append(np.array([[int(x) for x in y.strip().split()] 
          for y in lines[0:5]]))
        lines = lines[5:]

    return number_draw, np.array(cards)

def check_scores(scores):
    winners = []
    coords = np.where(scores.sum(axis=1) == 5)
    coords = list(zip(coords[0], coords[1]))
    for coord in coords:
        winners.append(coord[0])
   
    coords = np.where(scores.sum(axis=2) == 5)
    coords = list(zip(coords[0], coords[1]))
    for coord in coords:
        winners.append(coord[0])
    winners = list(set(winners))
    return winners

def get_raw_card_score(card, mask):
    return card[~mask].sum()

def part1(number_draw, cards):
    scores = np.zeros_like(cards, dtype=bool)
    while number_draw and len(check_scores(scores)) == 0:
        pick = number_draw.pop(0)
        scores += (cards == pick)

    winners = check_scores(scores)
    for winner in winners:
        raw_score = get_raw_card_score(cards[winner], scores[winner])
        
        msg = 'Part 1: raw score is {}, pick is {}, final score is {}'
        msg = msg.format(raw_score, pick, raw_score * pick)
        print(msg)

def part2(number_draw, cards):
    scores = np.zeros_like(cards, dtype=bool)
    while number_draw and (len(check_scores(scores)) < scores.shape[0] - 1):
        pick = number_draw.pop(0)
        scores += (cards == pick)

    winners = check_scores(scores)
    card_set = set(range(scores.shape[0]))
    missing = card_set.difference(set(winners))
    last_card = list(missing)[0]
    # ok we have the last card now, but it hasn't "won" yet.
    while number_draw and len(check_scores(scores)) < scores.shape[0]:
        pick = number_draw.pop(0)
        scores += (cards == pick)


    raw_score = get_raw_card_score(cards[last_card], scores[last_card])
    msg = 'Part 2: last card is {}, raw score is {}, pick is {}, final score is {}'
    msg = msg.format(last_card, raw_score, pick, raw_score * pick)
    print(msg)


if __name__ == '__main__':
    is_test = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            is_test = True

    number_draw, cards = get_data(is_test)
    part1(number_draw[:], cards)
    part2(number_draw[:], cards)
