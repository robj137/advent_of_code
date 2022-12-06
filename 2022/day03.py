import string
import sys

def get_priority(x):
    return 1 + (string.ascii_lowercase + string.ascii_uppercase).index(x)

if __name__ == '__main__':
    #with open('inputs/day03.test.txt') as f:
    with open('inputs/day03.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    sacks = []
    for line in lines:
        c1, c2 = line[0:len(line)//2], line[len(line)//2:]
        sacks.append([c1, c2, set(c1).intersection(c2), line])
    
    priorities = [get_priority(list(x[2])[0]) for x in sacks]
    print('part 1:', sum(priorities))

    groups = []
    for g in range(len(sacks)//3):
        groups.append([sacks[3*g][-1],  sacks[3*g+1][-1], sacks[3*g+2][-1]])

    badges = [set(x[0]).intersection(x[1]).intersection(x[2]).pop() for x in groups]
    print('part 2:', sum([get_priority(x) for x in badges]))
