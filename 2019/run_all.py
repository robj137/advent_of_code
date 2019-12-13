from datetime import datetime as dt
import day01
import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11

begin = dt.now()
days = [day01, day02, day03, day04, day05, day06, day07, day08, day09, day10, day11]
for day in days:
    print(day)
    day.main()
diff_time = dt.now() - begin
print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
