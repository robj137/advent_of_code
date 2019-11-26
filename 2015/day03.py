from collections import defaultdict

house_dict = defaultdict(int)

def move(current_location, step):
  x, y = current_location
  if step == '>':
    x += 1
  if step == '<':
    x -= 1
  if step == '^':
    y += 1
  if step == 'v':
    y -= 1
  return x, y

def main():
  with open('inputs/day3.txt') as f:
    directions = f.readline().strip()

  location1 = (0,0)
  location2 = (0,0)
  house_dict[location1] += 1
  house_dict[location2] += 1
  for i, step in enumerate(directions):
    if i%2 == 0:
      location1 = move(location1, step)
      house_dict[location1] += 1
    else:
      location2 = move(location2, step)
      house_dict[location2] += 1

  print(len(house_dict.keys()))

if __name__ == '__main__':
  main()


