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
    
    return np.array([[int(y) for y in list(x)] for x in lines])

if __name__ == '__main__':
    stand = get_data()
    X, Y = stand.shape
    
    visible = np.zeros((X, Y), dtype=bool) # boolean array for tree visibility
    scenic = np.zeros((X, Y), dtype=int)
    
    for i in range(X):
        for j in range(Y):
            val = stand[i, j]
            arrs = [
                np.flip(np.array(stand[i, :j])), # look up, or is it left? ;)
                np.array(stand[i, j+1:]), # look down
                np.flip(np.array(stand[:i, j])), # look left
                np.array(stand[i+1:, j]), # look right
            ]
            visible[i, j] = np.sum([np.all(val > x) for x in arrs])
            scenic[i, j] = np.prod([get_viewing_distance(val, x) for x in arrs])
    
    print('part 1:', np.sum(visible))
    print('part 2:', np.max(scenic))
