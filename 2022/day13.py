import numpy as np
import heapq
import functools

def get_data():
    with open('inputs/day13.txt') as f:
    #with open('inputs/day13.test.txt') as f:
        packet_data = f.read()

    packets = packet_data.split("\n\n")
    packets = [[eval(x.split('\n')[0]), eval(x.split('\n')[1])] for x in packets]
    return packets

def compare(left, right):
    t_l = type(left)
    t_r = type(right)
    if t_l != t_r:
        if t_l == int and t_r == list:
            return compare([left], right)
        else:  
            return compare(left, [right])
    if t_l == int:
        #comparing ints
        if left < right:
            return 1
        if left > right:
            return -1
        return 0
    # now it's interesting, we have two lists
    left = left[:]
    right = right[:]
    while len(left) and len(right):
        val = compare(left.pop(0), right.pop(0))
        if val:
            return val
        # ok, we've iterated through.
    if len(right) > len(left):
        return 1
    if len(right) < len(left):
        return -1
    return 0

def get_full_packets():
    packets = get_data()
    new_packets = []
    for p1, p2 in packets:
        new_packets.extend([p1, p2])
    new_packets.append([[2]])
    new_packets.append([[6]])

    return new_packets

if __name__ == '__main__':
    packet_pairs = get_data()
    #p = packets[5]
    #print(p, compare(p[0], p[1]))
    indices = [i+1 for i in range(len(packet_pairs)) if compare(packet_pairs[i][0], packet_pairs[i][1]) == 1]

    print('Part 1:', sum(indices))

    packets = get_full_packets()
    packets.sort(key=functools.cmp_to_key(compare))
    packets.reverse()
    ndx1 = 1+packets.index([[2]])
    ndx2 = 1+packets.index([[6]])
    print('Part 2:', ndx1*ndx2)
