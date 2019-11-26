import re
import numpy as np
from collections import defaultdict
import heapq

def get_graph():
    with open('inputs/day9.txt') as f:
        distances = [x.strip() for x in f.readlines()]
    cities = set()
    distance_graph = defaultdict(int)
    pattern = '([A-Za-z]+) to ([A-Za-z]+) = ([0-9]+)'
    for line in distances:
        result = re.search(pattern, line)
        if result:
            c1, c2, distance = result.groups()
            cities.add(c1)
            cities.add(c2)
        distance_graph[(c1,c2)] = int(distance)
        distance_graph[(c2,c1)] = int(distance)
    cities = list(cities)
    for city in cities:
        distance_graph[('Start', city)] = 0
        distance_graph[(city, 'Start')] = 0
    return distance_graph, cities

def compute(city, cost, cities, path, path_dict, graph):
    path.append(city)
    if len(path) > 1:
        cost += graph[(path[-2], path[-1])]
    for i, city in enumerate(cities):
        new_city = cities[i]
        other_cities = cities[0:i] + cities[i+1:]
        compute(new_city, cost, other_cities, path[:], path_dict, graph)
    if len(cities) == 0:
        path_dict['-'.join(path)] = cost

def path_search(graph, cities):
    path = []
    path_dict = {}

    compute('Start', 0, cities, path, path_dict, graph)
    
    key_min = min(path_dict.keys(), key=(lambda k: path_dict[k]))
    key_max = max(path_dict.keys(), key=(lambda k: path_dict[k]))
    return key_min, path_dict[key_min], key_max, path_dict[key_max]

def main():
    #with open('inputs/day8.txt') as f:
       
    graph, cities = get_graph()
    path1, cost1, path2, cost2 = path_search(graph, cities)
    
    print('Part 1: Shortest Distance is {}'.format(cost1))
    print('Part 2: Longest Distance is {}'.format(cost2))

if __name__ == '__main__':
  main()

