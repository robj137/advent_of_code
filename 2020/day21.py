import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


def get_data(is_test=False):
    if is_test:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day21.test.txt'
    else:
        in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day21.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
    

    rule_pattern = r'^(.*) \(contains (.*)\)$'
    pattern_re = re.compile(rule_pattern)
    rules = {}
    messages = []
    rules = []
    for line in lines:
        groups = pattern_re.search(line).groups()
        ingredients = [x.strip() for x in groups[0].split(' ')]
        allergens = [x.strip() for x in groups[1].split(',')]
        rules.append([ingredients, allergens])
    
    ingredient_set = set()

    allergy_dict = {}
    for ingredients, allergens in rules:
        ingredient_set.update(ingredients)
        for allergen in allergens:
            if allergen not in allergy_dict:
                allergy_dict[allergen] = set(ingredients)
            else:
                allergy_dict[allergen] = allergy_dict[allergen].intersection(set(ingredients))

    possible_ingredients = set()
    for allergen in allergy_dict:
        possible_ingredients.update(allergy_dict[allergen])
    safe_ingredients = ingredient_set.difference(possible_ingredients)
    
    n_safe_ingredients = 0
    for ingredients, allergens in rules:
        for ing in ingredients:
            if ing in safe_ingredients:
                n_safe_ingredients += 1

    print('n saafe ingredients', n_safe_ingredients)

    dangerous_ingredients = {}
    while sum([x for x in map(lambda x: len(allergy_dict[x]), allergy_dict)]):
        for allergen in allergy_dict:
            ingredients = allergy_dict[allergen]
            if len(ingredients) == 1:
                spoken_ingredient = ingredients.pop()
                dangerous_ingredients[allergen] = spoken_ingredient
                for a2 in allergy_dict:
                    i2 = allergy_dict[a2]
                    if spoken_ingredient in i2:
                        allergy_dict[a2].remove(spoken_ingredient)

    keys = [x for x in dangerous_ingredients.keys()]
    keys.sort()
    ingredients = [dangerous_ingredients[x] for x in keys]
    print(','.join(ingredients))
    return allergy_dict


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
    ingredients = get_data(is_test)
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
