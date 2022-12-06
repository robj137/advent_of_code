def get_score(line, result=None):
    op, sec = line.split(' ')
    if not result:
        shape_score = ord(sec) - 87
        outcome_score = 3 * ((ord(sec) - ord(op) - 23 + 1)%3 - 1) + 3
    else:
        outcome_score = 3*(ord(sec)-88)
        shape_score =  get_required_shape_score(sec, op)
    return shape_score + outcome_score

def get_required_shape_score(result, op):
    # result = 1, 2, 3 (lose, draw, win
    # op = 1 (x), 2 (Y), 3 (Z)
    result = ord(result) - 88
    op = ord(op) - 65
    return (op + result - 1) % 3 + 1

if __name__ == '__main__':
    #with open('inputs/day02.test.txt') as f:
    with open('inputs/day02.txt') as f:
        lines = [x.strip() for x in f.readlines()]

    scores_1 = [get_score(x) for x in lines]
    #print(scores_1)
    print('part 1:', sum(scores_1))
    scores_2 = [get_score(x, 1) for x in lines]
    #print(scores_1)
    print('part 2:', sum(scores_2))
