import datetime as dt
from collections import Counter
from datetime import datetime as dt

def get_data():
    in_file = 'inputs/day02.txt'
    with open(in_file) as f:
        lines = f.readlines()
    passwords = [x.strip() for x in lines]
    passwords = [x.split(' ') for x in passwords]
    entries = []
    for a, b, c in passwords:
        d = {}
        d['lo'], d['hi'] = [int(x) for x in a.split('-')]
        d['character'] = b.replace(':', '')
        d['password'] = c
        d['n'] = Counter(d['password'])[d['character']]
        d['is_valid_a'] = 1 if d['n'] >= d['lo'] and d['n'] <= d['hi'] else 0
        candidates = [c[d['lo'] - 1], c[d['hi'] - 1]]
        if candidates[0] == candidates[1]:
            candidates = []
        d['is_valid_b'] = 1 if d['character'] in candidates else 0
        entries.append(d)
    return entries


def main():
    data = get_data()
    n_valid_a = 0
    n_valid_b = 0
    for d in data:
        n_valid_a += d['is_valid_a']
        n_valid_b += d['is_valid_b']
    print(n_valid_a, n_valid_b)

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
