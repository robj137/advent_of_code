import numpy as np

def get_viewing_distance(val, arr):
    if len(arr) == 0:
        return 0
    for i, height in enumerate(arr):
        if height >= val:
            break
    return i + 1

def get_data():
    with open('inputs/day08.txt') as f:
    #with open('inputs/day08.test.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    
    stand = np.array([[int(y) for y in list(x)] for x in lines])
    return stand

if __name__ == '__main__':
    stand = get_data()
    X, Y = stand.shape
    
    visible = np.zeros((X, Y), dtype=bool) # boolean array for tree visibility
    scenic = np.zeros((X, Y))
    
    for i in range(X):
        for j in range(Y):
            val = stand[i, j]
            arrs = []
            arrs.append(np.flip(np.array(stand[i, :j]))) # look up, or is it left? ;)
            arrs.append(np.array(stand[i, j+1:])) # look down
            arrs.append(np.flip(np.array(stand[:i, j]))) # look left
            arrs.append(np.array(stand[i+1:, j])) # look right
            visible[i, j] = np.sum([np.all( val > x) for x in arrs])
            scenic[i, j] = np.prod([get_viewing_distance(val, x) for x in arrs])
    
    print('part 1:', int(np.sum(visible)))
    print('part 2:', int(np.max(scenic)))
