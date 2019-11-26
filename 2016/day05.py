import datetime as dt
import hashlib

def part_a():
  door_id = 'abc'
  door_id = 'uqwqemis'
  password = ''
  num = 0
  while len(password) < 8:
    if num%100000 == 0:
      print('on round {} and the current password is {}'.format(num, password))
    h = hashlib.md5((door_id + str(num)).encode()).hexdigest()
    if h[0:5] == '00000':   
      password += h[5]
    num += 1

  print('Part a: the password is {}'.format(password))

def part_b():
  door_id = 'abc'
  door_id = 'uqwqemis'
  password = '________'
  num = -1
  print('Password:\n{}'.format(password))
  while '_' in password:
    num += 1
    h = hashlib.md5((door_id + str(num)).encode()).hexdigest()
    if h[0:5] == '00000':
      place = h[5]
      character = h[6]
      try: 
        assert int(place) < len(password)
      except (AssertionError, ValueError):
        continue
      place = int(place)
      if password[place] == '_':
        password_l = list(password)
        password_l[place] = character
        password = ''.join(password_l)
        print('Round {}\nPassword: {}'.format(num, password))

  print('Part b: the password is {}'.format(password))


def main():
  #part_a()
  part_b()

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
