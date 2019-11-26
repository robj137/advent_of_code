import datetime as dt

def next2(current, d):
  if current == 1:
    return 3 if d == 'D' else 1
  if current == 2:
    return 3 if d == 'R' else 6 if d == 'D' else 2
  if current == 3:
    return 1 if d == 'U' else 2 if d == 'L' else 4 if d == 'R' else 7 if d == 'D' else 3
  if current == 4:
    return 3 if d == 'L' else 8 if d == 'D' else 4
  if current == 5:
    return 6 if d == 'R' else 5
  if current == 6:
    return 2 if d == 'U' else 5 if d == 'L' else 7 if d == 'R' else 'A' if d == 'D' else 6
  if current == 7:
    return 3 if d == 'U' else 6 if d == 'L' else 8 if d == 'R' else 'B' if d == 'D' else 7
  if current == 8:
    return 4 if d == 'U' else 7 if d == 'L' else 9 if d == 'R' else 'C' if d == 'D' else 8
  if current == 9:
    return 8 if d == 'L' else 9
  if current == 'A':
    return 6 if d == 'U' else 'B' if d == 'R' else 'A'
  if current == 'B':
    return 7 if d == 'U' else 'A' if d == 'L' else 'C' if d == 'R' else 'D' if d == 'D' else 'B'
  if current == 'C':
    return 8 if d == 'U' else 'B' if d == 'L' else 'C'
  if current == 'D':
    return 'B' if d == 'U' else 'D'

def next1(current, d):
  if current == 1:
    return 2 if d == 'R' else 4 if d == 'D' else 1
  if current == 2:
    return 1 if d == 'L' else 3 if d == 'R' else 5 if d == 'D' else 2
  if current == 3:
    return 2 if d == 'L' else 6 if d == 'D' else 3
  if current == 4:
    return 1 if d == 'U' else 5 if d == 'R' else 7 if d == 'D' else 4
  if current == 5:
    return 2 if d == 'U' else 4 if d == 'L' else 6 if d == 'R' else 8 if d == 'D' else 5
  if current == 6:
    return 3 if d == 'U' else 5 if d == 'L' else 9 if d == 'D' else 6
  if current == 7:
    return 4 if d == 'U' else 8 if d == 'R' else 7
  if current == 8:
    return 5 if d == 'U' else 7 if d == 'L' else 9 if d == 'R' else 8
  if current == 9:
    return 8 if d == 'L' else 6 if d == 'U' else 9

def main():
  with open('inputs/day2.txt') as f:
    lines = [x.strip() for x in f.readlines()]

  code1 = []
  current = 5
  for l in lines:
    for d in l:
      current = next1(current, d)
    code1.append(current)  

  code2 = []
  current = 5
  for l in lines:
    for d in l:
      current = next2(current, d)
    code2.append(current)  

  print('Part a: the bathroom code is {}'.format(''.join([str(x) for x in code1])))
  print('Part b: the real bathroom code is {}'.format(''.join([str(x) for x in code2])))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
