import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import datetime as dt

def main():
  with open('inputs/day4.txt') as f:
    lines = sorted([x.strip() for x in f.readlines()])
  

  current_guard = 0
  guard_dict = defaultdict(list)
  begin = 0
  end = 0
  for line in lines:
    if 'Guard' in line:
      begin = end = current_guard = 0
      current_guard = int(line.split('#')[1].split(' ')[0])
    if 'falls asleep' in line:
      begin = int(line.split(':')[1].split(']')[0])
    if 'wakes up' in line:
      end = int(line.split(':')[1].split(']')[0])
      for minute in range(begin, end):
        guard_dict[current_guard].append(minute)

  guard_minutes_dict = {}
  for guard in guard_dict:
    times = np.zeros(60)
    minute_count = Counter(guard_dict[guard])
    for minute in minute_count.keys():
      times[minute] = minute_count[minute]
    guard_minutes_dict[guard] = times
  guard_df = pd.DataFrame(guard_minutes_dict)
  df_sums = guard_df.sum()
  guard = df_sums.idxmax()
  max_minute = guard_df[guard].idxmax()
  print('Part a: ID * Minute of selected guard ({}) : {}'.format(guard, int(guard)*int(max_minute)))

  max_guard = guard_df.max()
  max_guard_id = max_guard.idxmax()
  max_guard_value = guard_df.max().loc[max_guard_id]
  #print(guard_df[107])
  minute_value = guard_df[max_guard_id].idxmax()
  print('Part b: Sleepy Guard ({}) times Sleepy Minute ({}) : {}'
        .format(max_guard_id, minute_value,minute_value * max_guard_id))


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
