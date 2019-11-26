import re
import string
import copy
import datetime as dt

def main():
  with open('inputs/day7.txt') as f:
    instructions = [re.search('Step (\w) must be finished before step (\w) can begin', x.strip()).groups() for x in f.readlines()]

  dependency_dict = {x:[] for x in string.ascii_uppercase}
  for instruction in instructions:
    req = instruction[0]
    dep = instruction[1]
    dependency_dict[dep].append(req)
  time1 = process(copy.deepcopy(dependency_dict), 1)
  time2 = process(copy.deepcopy(dependency_dict), 5)
  print('Part a: It takes {} seconds to process with {} worker(s)'.format(time1, 1))
  print('Part b: It takes {} seconds to process with {} worker(s)'.format(time2, 5))

def get_thread():
  thread = {}
  thread['time_left'] = 0
  thread['processing'] = None
  return thread

def process_dict(dependency_dict, queue, finished):
  for step in finished:
    for key in sorted(dependency_dict.keys()):
      if step in dependency_dict[key]:
        # if a letter is 'finished', pop it off any dependency lists in the dict
        dependency_dict[key].pop(dependency_dict[key].index(step))
  for key in sorted(dependency_dict.keys()):
    if len(dependency_dict[key]) == 0:
      # oh good, all dependencies are taken care of, so we remove this guy from the dictionary and
      # add it to the queue
      queue.append(key)
      del dependency_dict[key]
  # and we sort the queue to keep it alphabetical (jobs get popped off the top, so also reverse) 
  queue.sort()
  queue.reverse()

def process(dependency_dict, n_threads = 1):
  # pretty simple really. the dependency_dict has a key for each letter
  # the value for a key is a list of all that letter's dependencies
  # the dictionary gets updated, so once a letter is processed, it gets deleted from
  # the dictionary value until a letter only has an empty list. if that list is empty, 
  # the letter can begin to be processed, and gets added to the queue
  # once a letter is processed, it gets added to finished.
  # each second, check for available workers (threads) to pick up anything in the queue (if there
  # is anything)
  # each worker (thread) keeps track of what it's working on and how much longer it has to go
  threads = [get_thread() for _ in range(n_threads)]
  queue = []
  finished = []

  time = 0
  while len(finished) < 26:
    time += 1
    for thread in threads:
      if thread['time_left'] == 1:
        finished.append(thread['processing'])
        thread['processing'] = None
      if thread['time_left'] > 0:
        thread['time_left'] -= 1
    # do some cleanup work on the dictionary
    process_dict(dependency_dict, queue, finished)
    for thread in threads:
      if not thread['processing']:
        if queue:
          # we have an idle worker and something for them to do!
          step = queue.pop()
          thread['processing'] = step
          thread['time_left'] = 60 + ord(step) - 64
  return time-1

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
