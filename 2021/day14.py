import numpy as np
import sys
from collections import Counter
from datetime import datetime as dt

def get_data(is_test=True):
    path = 'inputs/day14.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()

    rules = {}
    for line in lines:
        if len(line) > 1 and '->' not in line:
            template = line.strip()
        elif len(line) > 1:
            pair, insertion = line.strip().split(' -> ')
            rules[pair] = insertion

    return template, rules

def run_rules(template, rules):
    t = template
    inserts = []
    for i in range(len(t)-1):
        pair = t[i:i+2]
        inserts.append(rules[pair])
    
    new_t = ''.join([''.join(x) for x in zip(t, inserts)]) + t[-1]
    return new_t

def part1(template, rules):
    t = template[:]
    v = []
    o = []
    for i in range(20):
        t = run_rules(t, rules)
        c = Counter(t)
        minimum = min(c, key=c.get)
        maximum = max(c, key=c.get)
        # print(i, c[maximum]-c[minimum])
        l = len(t)
        # print(i, l, c['V'], c['O'])
        v.append(c['V'])
        o.append(c['O'])
        print(i, l, c['V'], c['F'], c['B'], c['C'], c['H'], c['K'], c['N'], c['P'], c['S'], c['O'])
        # print(i, l, c['V']/l, c['F']/l, c['B']/l, c['C']/l, c['H']/l, c['K']/l, c['N']/l, c['P']/l, c['S']/l, c['O']/l)


    print(v)
    print(o)


def part2():
    maximum = 41781441855489


if __name__ == '__main__':
    begin = dt.now()
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    template, rules = get_data(is_test)
    part1(template, rules)
    part1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
    #diff_time = dt.now() - part1_time
    #print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
