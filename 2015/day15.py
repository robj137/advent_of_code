import string
from datetime import datetime as dt
import re
from itertools import permutations
from iminuit import Minuit
import numpy as np

def get_input(is_test = False):
    path = 'inputs/day15.txt'
    if is_test:
        path = 'inputs/day15_alt.txt'
    with open(path) as f:
        lines = f.readlines()
    ingredient_names = []
    ingredient_values = []
    for line in lines:
        name, data = extract_ingredient_data(line)   
        ingredient_values.append(data)
        ingredient_names.append(name)
    ingredient_values = np.matrix(ingredient_values)
    return ingredient_names, ingredient_values

def extract_ingredient_data(l):
    pattern = '([A-Z][a-z]+): capacity (-?\d+), durability (-?\d+), '
    pattern += 'flavor (-?\d+), texture (-?\d+), calories (-?\d+)'
    result = re.search(pattern, l)
    if result:
        g = result.groups()
        name = g[0]
        data = [int(x) for x in g[1:]]
        return name, data

ingredients, proportions = get_input(False)
#ingredients, proportions = get_input(True)

def caloric_cost(x):
    X = np.append(x, 100 - np.sum(x))
    calorie_count = int(X * proportions[:,4])
    return calorie_count
    

def cost(x):
    """x is a numpy array, corresponding to first n-1 parameters"""
    
    # first off, add the final component to the parameter:
    X = np.append(x, 100 - np.sum(x))
    data = proportions[:, 0:4]
    score = -np.prod(X * data)
    return score

def cost_with_penalty(x):
    """x is a numpy array, corresponding to first n-1 parameters"""
    calorie_count = caloric_cost(x)
    # first off, add the final component to the parameter:
    X = np.append(x, 100 - np.sum(x))
    if True in (X < 0):
        return 0
    data = proportions[:, 0:4]
    score = -np.prod(X * data)
    penalty = np.exp(-0.5 * np.power(calorie_count - 500,2)/(np.power(4.1,2)))
    return score * penalty

def prettify_results(args):
    args = list(args)
    args.append(100 - sum(args))
    for i in range(len(args)):
        print('{}: {}'.format(ingredients[i], args[i]))

def get_initial_values(data):
    dim = data.shape[0] - 1
    base = 100 / (dim + 1)
    inits = []
    for i in range(dim):
        inits.append(np.random.normal(base, 1))
    return tuple(inits)

def get_limits(data):
    dim = data.shape[0] - 1
    return tuple(dim * [(0,100)])

def main():
    initial = get_initial_values(proportions)
    limits = get_limits(proportions)
    errors = tuple((proportions.shape[0] - 1)* [2])  
    m1 = Minuit.from_array_func(cost, initial, errors, limit=limits, errordef=1)
    m1.migrad()
    final_values = [round(x) for x in m1.args]
    final_cost = cost(np.array(final_values))
    calories = caloric_cost(np.array(final_values))
    print('Part 1: Final cost is {} (with {} calories)'.format(-final_cost, calories))
    prettify_results(final_values)
    
    #Part 2: Final cost with caloric constraint is 11171160.0 (with 500 calories)
    #Sprinkles: 27
    #Butter: 27
    #Frosting: 15
    #Sugar: 31

    m2 = Minuit.from_array_func(cost_with_penalty, initial, errors, limit=limits, errordef=1)
    m2.migrad()
    final_values = [round(x) for x in m2.args]
    final_cost = cost_with_penalty(np.array(final_values))
    calories = caloric_cost(np.array(final_values))
    print('Part 2: Final cost with caloric constraint is {} (with {} calories)'
        .format(-final_cost, calories))
    prettify_results(final_values)
    
    
if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
