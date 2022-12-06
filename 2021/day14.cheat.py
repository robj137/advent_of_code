from collections import defaultdict, Counter
from pathlib import Path
path = Path("inputs/day14.txt")

def read_input(path):
    data = path.read_text().strip().split("\n")
    template = data[0]
    rules = dict(map(lambda x : tuple(map(lambda y : y.strip(), x.split("->"))), data[2:]))
    return template, rules

template, rules = read_input(path)

def count_occurences(template, rules, n_steps = 0):
    counter = Counter(template)
    polymer = Counter(["".join(i) for i in zip(template, template[1:])]) # groups of two letters
    print(polymer)
    for _ in range(n_steps):
        curr = defaultdict(int)
        for k in polymer.keys():
            curr[k[0] + rules[k]] += polymer[k]
            curr[rules[k] + k[1]] += polymer[k]
            counter[rules[k]] += polymer[k]
        polymer = curr
        print(len(polymer))
    return counter.most_common()[0][1] - counter.most_common()[-1][1]

print(count_occurences(template, rules, 10))
print(count_occurences(template, rules, 40))
