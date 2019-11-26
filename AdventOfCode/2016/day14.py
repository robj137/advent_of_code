import re
import hashlib
import numpy as np
from datetime import datetime as dt
from collections import defaultdict
import heapq

salt = 'qzyelonm' #'abc'

def perform_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

def gimme_more_hash_candidates(hash_candidates, pt_2 = False):
    n_current = len(hash_candidates)
    rx3 = re.compile(r'(.)\1{2,}')
    rx5 = re.compile(r'(.)\1{4,}')
    for i in range(n_current, n_current + 5000):
        s = salt + str(i)
        new_hash = perform_hash(s)
        if pt_2:
            for i in range(2016):
                new_hash = perform_hash(new_hash)
        hash_candidates.append([new_hash, rx3.findall(new_hash), rx5.findall(new_hash)])

def do_part(pt_2 = False):
    
    hash_candidates = []
    

    keys = []

    this_hash_ndx = 0
    while len(keys) < 64:
        if this_hash_ndx + 1000 > len(hash_candidates):
            gimme_more_hash_candidates(hash_candidates, pt_2)
        this_hash = hash_candidates[this_hash_ndx]
        if this_hash[1]:
            repeated = this_hash[1][0]
            i = this_hash_ndx+1
            while i <= this_hash_ndx + 1000:
                if repeated in hash_candidates[i][2]:
                    keys.append((this_hash_ndx, hash))
                    break
                i += 1
        this_hash_ndx += 1
    return keys

def part1():
    keys = do_part(False)
    print('Part 1: 64th key produced at index {}'.format(keys[-1][0]))


def part2():
    keys = do_part(True)
    print('Part 2: 64th key produced at index {}'.format(keys[-1][0]))


def main():
    
    part1()
    part2()

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
