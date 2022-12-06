

#with open('inputs/day02.test.txt') as f:
with open('inputs/day02.txt') as f:
    lines = f.readlines()


x = 0
z = 0
dirs = []
for l in lines:
    a, b = l.split(' ')
    b = int(b)
    if a == 'forward':
        x += b
    elif a == 'up':
        z = z - b
    else:
        z = z + b

print(x*z)

x = 0
aim = 0
z = 0

for l in lines:
    a, b = l.split(' ')
    b = int(b)
    if a == 'down':
        aim += b
    elif a == 'up':
        aim -= b
    else:
        x += b
        z += aim * b

print(x*z)
