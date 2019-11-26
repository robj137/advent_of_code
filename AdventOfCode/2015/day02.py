

def main():
  dims = []
  with open('inputs/day2.txt') as f:
    for line in f:
      dims.append(sorted([int(x) for x in line.strip().split('x')]))

  area = []
  length = []
  for dim in dims:
    area.append( 3*dim[0]*dim[1] + 2*dim[0]*dim[2] + 2*dim[1]*dim[2])
    length.append( 2*dim[0] + 2*dim[1] + dim[1]*dim[0]*dim[2])
  print(sum(area))
  print(sum(length))

if __name__ == '__main__':
  main()


