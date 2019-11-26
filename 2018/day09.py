import sys
from collections import Counter, deque, defaultdict
import datetime as dt


def main():
  input_players = 486
  last_marble_worth = 70833
  max_score_a = play_marble_game(input_players, last_marble_worth) 
  max_score_b = play_marble_game(input_players, 100*last_marble_worth) 

  print('Part a: Winning elf\'s score for {} players and last marble worth {}: {}'
        .format(input_players, last_marble_worth, max_score_a))
  print('Part b: Winning elf\'s score for {} players and last marble worth {}: {}'
        .format(input_players, 100*last_marble_worth, max_score_b))

def play_marble_game(n_players, n_marbles):
  # My original entry used np arrays. Part 2 took like half an hour ..., 
  # but half the fun of these is figuring out how to do it a better way, and so I learned about
  # double-ended queues (deques) :)
  circle = deque([0])
  elves = [0]*n_players
  for marble in range(1,n_marbles+1):
    if marble % 23 == 0:
      circle.rotate(7)
      elves[marble%n_players] += marble + circle.pop()
      circle.rotate(-1)
    else:
      circle.rotate(-1)
      circle.append(marble)

  return max(elves)
if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
