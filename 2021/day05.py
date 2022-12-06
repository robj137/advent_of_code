import numpy as np
import sys
import re
from collections import defaultdict

def get_data(is_test=True):
    path = 'inputs/day05.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    
    cards = []
    while lines and lines[0] == '\n':
        lines.pop(0)
        cards.append(np.array([[int(x) for x in y.strip().split()] 
          for y in lines[0:5]]))
        lines = lines[5:]
    pattern = '(\d+),(\d+) -> (\d+),(\d+)'
    coord_pairs = []
    for line in lines:
        s = re.search(pattern, line)
        if s:
            x1, y1, x2, y2 = s.groups()
            coord_pairs.append([(int(x1), int(y1)), (int(x2), int(y2))])

    return np.array(coord_pairs)

def look_at_lines(coord_pairs, cardinal_only = False):
    hot_spots = defaultdict(int)
    for coord_a, coord_b in coord_pairs:
        p = coord_b - coord_a
        p1 = int(p[0]/np.linalg.norm(p[0])) if p[0] else 0
        p2 = int(p[1]/np.linalg.norm(p[1])) if p[1] else 0
        p = np.array([p1, p2])  # "normalized" step vector
        c = coord_a  # start at the beginning
        if cardinal_only and np.linalg.norm(p) != 1.0:
            continue
        hot_spots[tuple(c)] += 1
        while (c != coord_b).any():
            c += p
            hot_spots[tuple(c)] += 1

    return len([x for x in filter(lambda x: hot_spots[x] >= 2, hot_spots)])

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    p1 = look_at_lines(data.copy(), cardinal_only=True)
    p2 = look_at_lines(data.copy(), cardinal_only=False)
    print(p1, p2)
