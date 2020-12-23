import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False, part2=False):
    if is_test and not part2:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day19.test.txt'
    elif is_test and part2:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day19.test2.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day19.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
    

    rule_pattern = r'^(\d+): (.*)$'
    message_pattern = r'^[ab]*$'
    rule_re = re.compile(rule_pattern)
    message_re = re.compile(message_pattern)
    rules = {}
    messages = []
    for line in lines:
        if rule_re.search(line):
            rule_number, rule = rule_re.search(line).groups()
            if part2:
                if rule_number == '8':
                    rule = '(?:42 | 42 8)'
                    rule = '(?: 42 | 42 (?: 42 | 42 (?: 42 | 42 (?: 42 | 42 (?: 42 | 42 )))))'
                    #for i in range(100):
                    #    rule = rule.replace('8', '(?:42 | 42 8)')
                    #rule = rule.replace(' 8', ' ')
                if rule_number == '11':
                    rule = '(?:42 31 | 42 11 31)'
                    rule = '(?: 42 31 | 42 (?: 42 31 | 42 (?: 42 31 | 42 (?: 42 31 | 42 (?: 42 31 | 42 31 ) 31 ) 31 ) 31 ) 31 )'
                    #for i in range(100):
                    #    rule = rule.replace('11', '(?:42 31 | 42 11 31)')
                    #rule = rule.replace(' 11', ' ')
            rule = rule.replace('"', '')
            rule = [try_to_int(x) for x in rule.split(' ')]
            if '|' in rule:
                rule = ['(?:'] + rule + [')']


            rules[int(rule_number)] = rule 
        elif len(line) < 1:
            continue
        elif message_re.search(line):
            messages.append(line)

    has_numeric = True
    n_rules_beginning = len(rules)
    while has_numeric:
        has_numeric = False
        keys = [x for x in rules.keys()]
        for rule_number in keys:
            rule = rules[rule_number]
            to_replace = []
            for element in rule:
                if type(element) == int:
                    to_replace.append(element)
            to_replace = list(set(to_replace))
            if len(to_replace) >0:
                has_numeric = True
            for element in to_replace:
                sub_rule = rules[element]
                while element in rule:
                    ndx = rule.index(element)
                    rule = rule[:ndx] + sub_rule + rule[ndx+1:]
            rules[rule_number] = rule

    n_rules_ending = len(rules)
    for rule_number in rules:
        rules[rule_number] = '^' +  ''.join(rules[rule_number]) + '$'
    return rules, messages

def try_to_int(val):
    if val.isnumeric():
        return int(val)
    return val


def run(rules, messages):
    pattern = rules[0]
    matcher = re.compile(pattern)
    n_matches = 0
    for m in messages:
        if matcher.search(m):
            n_matches += 1
    return n_matches

def part2(data):
    pass

if __name__ == '__main__':
    begin = dt.now()
    is_test = False
    rules, messages = get_data(is_test)
    part_1_answer = run(rules, messages)
    part_1_time = dt.now()
    diff_time = dt.now() - begin
    print('Part 1: {}'.format(part_1_answer))
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    rules, messages = get_data(is_test, part2=True)
    part_2_answer = run(rules, messages)
    diff_time = dt.now() - part_1_time
    print('Part 12 {}'.format(part_2_answer))
    
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))