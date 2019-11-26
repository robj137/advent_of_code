from heapq import heappop, heappush
import datetime as dt

begin = dt.datetime.now()
depth = 5616
target_x, target_y = (10,785)
maze = {(0, 0): 0, (target_x, target_y): 0}

def get(x, y, raw=False):
    v = maze.get((x, y))
    if v is None:
        if x == 0:
            v = 48271 * y
        elif y == 0:
            v = 16807 * x
        else:
            v = ((get(x - 1, y, True) + depth) % 20183) * ((get(x, y - 1, True) + depth) % 20183)
        maze[(x, y)] = v
    return v if raw else (v + depth) % 20183 % 3

print(sum(get(x, y) for x in range(target_x + 1) for y in range(target_y + 1)))
diff_time = dt.datetime.now() - begin
print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

def estimate(w, x, y, t):
    return w + abs(x) + abs(y) + (0 if t == 1 else 7), w, x, y, t

q = [(0, 0, target_x, target_y, 1)]
ws = {}
while q:
    _, w, x, y, t = heappop(q)
    if (x, y, t) in ws and ws[(x, y, t)] <= w:
        continue
    ws[(x, y, t)] = w
    if x == 0 and y == 0 and t == 1:
        break
    heappush(q, estimate(w + 7, x, y, -(get(x, y) + t) % 3))
    for x, y in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
        if x < 0 or y < 0 or get(x, y) == t or (x, y, t) in ws:
            continue
        e = w + 1 + abs(target_x - x) + abs(target_y - y) + (0 if t == 1 else 7)
        heappush(q, estimate(w + 1, x, y, t))
print(w)
diff_time = dt.datetime.now() - begin
print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
