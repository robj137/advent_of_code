import pandas as pd
import numpy as np
import datetime as dt

class Elf:
  def __init__(self, recipe_index, recipe_value):
    self.current_recipe_index = recipe_index
    self.current_recipe_value = recipe_value

def main():
  scoreboard = [3,7]

  check = 920831
  elf1 = Elf(0, 3)
  elf2 = Elf(1, 7)

  while len(scoreboard) < 920831+10:
    scoreboard.extend(create_new_recipes([elf1, elf2]))
    pick_new_recipes([elf1, elf2], scoreboard)

  recipe_string = ''.join([str(x) for x in scoreboard[-10:]])
  print('Part a: Scores of the 10 recipes immediately after {}: {}'.format(check, recipe_string))
  
  check = str(check)
  not_found = True
  tick=0
  prev_length = 0
  while not_found:
    tick += 1
    if tick%1000000 == 0:
      #print(tick, elf1.current_recipe_index, elf2.current_recipe_index, len(scoreboard))
      s = ''.join([str(x) for x in scoreboard[prev_length:len(scoreboard)]])
      if check in s:
        ndx = s.index(check) + prev_length
        print('Part b: there are {} recipes before {}'.format(ndx, check))
        not_found = False
      prev_length = len(scoreboard)
  #while scoreboard[-5:] != [5,9,4,1,4]:
    scoreboard.extend(create_new_recipes([elf1, elf2]))
    pick_new_recipes([elf1, elf2], scoreboard)
  
def pick_new_recipes(elf_list, scores):
  for elf in elf_list:
    elf.current_recipe_index = (elf.current_recipe_index + 1 + elf.current_recipe_value)%len(scores)
    elf.current_recipe_value = scores[elf.current_recipe_index]
  
def create_new_recipes(elf_list):
  return [int(x) for x in list( str( sum([x.current_recipe_value for x in elf_list]) ) ) ] 

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
