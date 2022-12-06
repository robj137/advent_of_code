#with open('inputs/day01.test.txt') as f:
with open('inputs/day01.txt') as f:
    lines = [x.strip() for x in f.readlines()]

elves = []
prev = None
for line in lines:
    if not prev:
        new_elf = []
        prev = 1
    if line:
        new_elf.append(int(line))
    else:
        elves.append(new_elf[:])
        prev = None
elves.append(new_elf[:])

elf_totals = [sum(x) for x in elves]

elf_totals.sort()
elf_totals.reverse()

print('part 1:', elf_totals[0])
print('part 2:', sum(elf_totals[0:3]))
