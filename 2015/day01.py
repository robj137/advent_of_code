from collections import Counter

def main():
  with open('inputs/day1.txt') as f:
    directions = f.readline().strip()

  c = Counter(directions)
  print(c['('] - c[')'])

  translate = {}
  translate['('] = 1
  translate[')'] = -1
  level = 0
  keep_going = True
  for i, step in enumerate(directions):
    level += translate[step]
    if keep_going:
      if level == -1:
        print("{} is the first step where Santa goes underground".format(i+1))
        keep_going = False
  print(level)

if __name__ == '__main__':
  main()

