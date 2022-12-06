import numpy as np
import sys
from collections import Counter

def get_data(is_test=True):
    path = 'inputs/day10.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    return [x.strip() for x in lines]

def is_corrupt(line):
    queue = []
    d = {'>': '<', ']': '[', ')': '(', '}': '{'}
    for el in line:
        if el in ['(', '[', '{', '<']:
            queue.append(el)
        if el in [')', ']', '}', '>']:
            if d[el] != queue[-1]:
                return el
            queue.pop()
    return ''

def is_complete(line):
    if is_corrupt(line) != '':
        return False
    c = Counter(line)
    if c['['] == c[']'] and c['<'] == c['>'] and c['('] == c[')'] and c['{'] == c['}']:
        return True
    return False

def complete_line(line):
    fixed = ''
    temp = ''
    while not is_complete(line + fixed + temp):
        for n in [')', '}', '>', ']']:
            if is_corrupt(line + fixed + n) == '':
                fixed += n
                if is_complete(line + fixed):
                    return fixed

def score_completed_line(fixed):
    c = Counter(fixed)
    rubric = {')': 1, ']': 2, '}': 3, '>': 4}
    score = 0
    for el in fixed:
        score *= 5
        score += rubric[el]
    return score

def part1(data):
    payout = {')': 3, ']': 57, '}': 1197, '>': 25137, '': 0}
    money = 0
    for line in data:
        money += payout[is_corrupt(line)]
    print('Part 1:', money)

def part2(data):
    incomplete = [x for x in data if is_corrupt(x) == '']
    completions = [complete_line(x) for x in incomplete]
    scores = sorted([score_completed_line(x) for x in completions])
    index = int(np.floor(len(scores) / 2))
    print('Part 2:', scores[index])

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
    part2(data)
