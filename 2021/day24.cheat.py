with open("inputs/day24.txt", 'r') as file:
    data = [x.strip('\n').strip().splitlines() for x in file.read().split('inp w\n')[1:]]
    print(data)
    non_matching = [e for e,x in enumerate(data[0]) if not all(data[y][e] == x for y in range(len(data)))]
    diffs = [[int(data[i][e].split()[-1]) for e in non_matching] for i in range(len(data))]
    q, mx, mn = [], [0] * 14, [0] * 14
    for a, x in enumerate(data):
        if diffs[a][0] == 1:
            q.append((a, diffs[a][2]))
        else:
            b, y = q.pop()
            delta = y + diffs[a][1]
            if not delta >= 0:
                a, b, delta = b, a, -delta
            mx[a], mx[b] = 9, 9 - delta
            mn[b], mn[a] = 1, 1 + delta
    print(''.join([str(x) for x in mx]))
    print(''.join([str(x) for x in mn]))
