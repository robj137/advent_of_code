import datetime as dt
from collections import Counter, defaultdict, deque
from datetime import datetime as dt
import numpy as np
import re
from copy import deepcopy


def get_data(is_test=False):
    if is_test:
        public_keys = [5764801, 17807724]
    else:
        public_keys = [16616892, 14505727]
    
    
    return public_keys


def guess_loop_size(subject_number, public_key):
    value = 1
    loops = 0
    while value != public_key:
        loops += 1
        value *= subject_number
        value = value % 20201227
    return loops

def handshake(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227

    return value

if __name__ == '__main__':
    begin = dt.now()
    is_test = False
    public_keys = get_data(is_test)
    loops = [guess_loop_size(7, x) for x in public_keys]
    loops = loops[::-1] # reverse
    pairs = [x for x in zip(public_keys, loops)]
    encryption_key1 = handshake(pairs[0][0], pairs[0][1])
    encryption_key2 = handshake(pairs[1][0], pairs[1][1])

    if encryption_key1 == encryption_key2:
        print("Part 1: Self-consistent Encryption Key is {}".format(encryption_key2))

    part_1_time = dt.now()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
