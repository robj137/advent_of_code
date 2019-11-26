import hashlib

def main():
  with open('inputs/day4.txt') as f:
    inp = f.readline().strip()

  for num in range(0, 10000000):
    if hashlib.md5((inp + str(num)).encode()).hexdigest()[0:6] == '000000':
      print('huzzah, {} is the first int to result in 6 zeros'.format(num))
if __name__ == '__main__':
  main()

