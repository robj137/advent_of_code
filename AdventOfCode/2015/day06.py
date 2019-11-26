import re
import numpy as np

def step(direction, coords, lights):
  x1, y1, x2, y2 = coords[0], coords[1], coords[2]+1, coords[3]+1
  if direction == 'on':
    lights[x1:x2,y1:y2] += 1
    #lights[x1:x2,y1:y2] = 1
  elif direction == 'off':
    lights[x1:x2,y1:y2] -= 1
    #lights[x1:x2,y1:y2] = 0
  else:
    lights[x1:x2,y1:y2] += 2
    #lights[x1:x2,y1:y2] = 1 - lights[x1:x2,y1:y2]

  lights[lights < 0] = 0

def main():
  instructions = []
  coords = []
  pattern = '(\d+),(\d+) through (\d+),(\d+)'
  with open('inputs/day6.txt') as f:
    for line in f:
      instructions.append('toggle' if 'toggle' in line else 'on' if 'turn on' in line else 'off')
      coords.append([int(x) for x in re.search(pattern, line).groups()])


  
  lights = np.zeros([1000,1000])
  print(np.sum(lights))
  for x, y in zip(instructions, coords):
    step(x, y, lights)
    print(x,y,np.sum(lights))

if __name__ == '__main__':
  main()

