import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re

class Bag:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules
        self.contents = {}
        self.contains_shiny_gold = False
    
    def add_contents(self, blurb):
        if blurb == 'no other bags.':
            return [None]
        blurb = [x.strip() for x in blurb.split(',')]
        pattern = '(\d) (\D*) bags?'
        contents = []
        for bag_blurb in blurb:
            p = re.compile(pattern)
            result = p.search(bag_blurb)
            if result:
                bag_name = result.groups()[1]
                bag_num = int(result.groups()[0])
                this_bag = self.rules.gimme_bag(bag_name)
                self.contents[bag_name] = {'num': bag_num, 'bag_instance': this_bag}


class Rules:
    def __init__(self, lines):
        self.lines = lines
        self.bag_dict = {}
        self.process_contents()
    
    def gimme_bag(self, name):
        if name in self.bag_dict:
            return self.bag_dict[name]
        bag = Bag(name, self)
        self.bag_dict[name] = bag
        return bag

    def process_contents(self):
        pattern = '^(.*) bags contain (.*)$'
        p = re.compile(pattern)

        for line in self.lines:
            a = p.search(line)
            if a:
                g = a.groups()
                key = g[0]
                bag = Bag(key, self)
                self.bag_dict[key] = bag
                bag.add_contents(g[1])


    def search_for_gold(self, bag):
        if bag.name == 'shiny gold' or bag.contains_shiny_gold:
            return 1
        if len(bag.contents) == 0:
            return 0
        content_scores = []
        for inner_bag_name in bag.contents:
            inner_bag = self.gimme_bag(inner_bag_name)
            content_scores.append(self.search_for_gold(inner_bag))
        if sum(content_scores) > 0:
            bag.contains_shiny_gold = True
            return 1
        return 0

    def get_bag_content_list(self, bag):
        content_list = []
        if type(bag) == str:
            bag = self.gimme_bag(bag)
        for inner_bag_name in bag.contents:
            for n in range(bag.contents[inner_bag_name]['num']):
                content_list.append(inner_bag_name)
        return content_list
            

def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day07.test2.txt'
    else:
        in_file = 'inputs/day07.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
 
    return lines


def get_rules():
    data = get_data(is_test=False)
    rules = Rules(data)
    return rules

def main():
    rules = get_rules()
    _ = [rules.search_for_gold(rules.gimme_bag(x)) for x in rules.bag_dict.keys()]
    n_bags = sum([x for x in map(lambda x: rules.gimme_bag(x).contains_shiny_gold, rules.bag_dict)])
    print(n_bags)

    inner_bags = {}
    counted_bags = defaultdict(int)
    uncounted_bags = rules.get_bag_content_list('shiny gold')
    
    while uncounted_bags:
        new_bag_name = uncounted_bags.pop()
        uncounted_bags.extend(rules.get_bag_content_list(new_bag_name))
        counted_bags[new_bag_name] += 1

    print(sum(map(lambda x: counted_bags[x], counted_bags)))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
