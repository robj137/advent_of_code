import numpy as np
import pandas as pd
import sys

def get_new_mask(df):
    pre_mask = np.round(df.mean() + 1e-8)
    o2_mask = [int(x) for x in pre_mask]
    co2_mask = [int(x) for x in 1-pre_mask]
    return o2_mask, co2_mask

def get_data(is_test=True):
    path = 'inputs/day03.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()
    lines = [list(x.strip()) for x in lines]
    lines = [[int(y) for y in x] for x in lines]
    df = pd.DataFrame(lines)
    return df

def iterate_for_rating(df, rating_name = 'o2'):
    rating_int = 0 if rating_name == 'o2' else 1
    for i in range(df.shape[1]):
        mask = get_new_mask(df)[rating_int]
        cut = df[i] == mask[i]
        df = df[cut]
        if df.shape[0] == 1:
            break
    
    rating_s = ''.join([str(int(x)) for x in df.iloc[0].tolist()])
    rating = int(rating_s, 2)
    return rating_s, rating

def part1(df):
    gamma_s = ''.join([str(int(x)) for x in np.round(df.mean(axis=0)).tolist()])
    gamma = int(gamma_s, 2)
    # just flip 1 <-> 0 from gamma to get epsilon:
    epsilon_s =  ''.join([str(1-int(x)) for x in gamma_s])
    epsilon = int(epsilon_s, 2)
    msg = 'Part 1: gamma rate = {}, epsilon rate = {}, power consumption = {}'
    msg = msg.format(gamma, epsilon, gamma * epsilon)
    print(msg)

def part2(df):
    df_o2 = df.copy()
    df_co2 = df.copy()

    o2_s, o2_rating = iterate_for_rating(df_o2, 'o2')
    co2_s, co2_rating = iterate_for_rating(df_co2, 'co2')

    msg = 'Part 2: o2_rating = {}, co2_rating = {}, life support rating = {}'
    msg = msg.format(o2_rating, co2_rating, o2_rating * co2_rating)
    print(msg)

if __name__ == '__main__':
    is_test = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            is_test = True

    data = get_data(is_test)
    part1(data)
    part2(data)
