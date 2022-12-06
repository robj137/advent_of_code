import numpy as np
import sys
from collections import Counter
from datetime import datetime as dt
import aoc_utils

packet_dict = {}

class Packet:
    def __init__(self, binary_rep, start_pos, parent=None):
        # already a string in binary representation
        # the bin_rep should contain everything about this particular packet.
        # easy if it's the root packet.
        # somewhat more difficult down the hole.
        # so the packet needs to be able to divvy up the payload and seed it
        # to generate child packets
        # if the bin_rep is a literal, 
        self.binary_rep = binary_rep
        self.start_pos = start_pos
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 0
        self.children = []
        self.version = int(binary_rep[start_pos:start_pos + 3], 2)
        self.type_id = int(binary_rep[start_pos+3:start_pos + 6], 2)
        br = binary_rep[start_pos:]
        #print(f'new packet, depth = {self.depth}, version = {self.version} and type id is {self.type_id}, and bin rep is {br}')
        self.literal_value = None
        self.length_type_id = None
        self.end_pos = None
        if self.type_id == 4: # literal, so let's unpack it and mvoe on
            # print('unpacking literal')
            self.unpack_literal()
            # the left over should just be zeros, as we should have already
            # demarced the end of the "packet"`
        else:
            self.parse_subpackages()

    def get_value(self):
        if self.type_id == 4:
            return self.literal_value
        elif self.type_id == 0:
            return sum([x.get_value() for x in self.children])
        elif self.type_id == 1:
            return np.prod([x.get_value() for x in self.children])
        elif self.type_id == 2:
            return min([x.get_value() for x in self.children])
        elif self.type_id == 3:
            return max([x.get_value() for x in self.children])
        elif self.type_id == 5:
            return 1 if self.children[0].get_value() > self.children[1].get_value() else 0
        elif self.type_id == 6:
            return 1 if self.children[0].get_value() < self.children[1].get_value() else 0
        elif self.type_id == 7:
            return 1 if self.children[0].get_value() == self.children[1].get_value() else 0

    def get_length(self):
        if self.end_pos:
            return 1 + self.end_pos - self.start_pos
        return None

    def parse_subpackages(self):
        length_type = int(self.binary_rep[self.start_pos + 6], 2)
        
        length_start = self.start_pos + 7
        sub_length = None
        sub_number = None
        sub_packet_pointer = length_start + 15 if length_type == 0 else length_start + 11
        # depends on if 0 or 1
        sub_length = int(self.binary_rep[length_start:sub_packet_pointer], 2)
        # print('length type and actual length is', length_type, sub_length, length_start, sub_packet_pointer)
        while sub_length:
            self.children.append(Packet(self.binary_rep, sub_packet_pointer, self))
            sub_packet_pointer = self.children[-1].end_pos + 1
            if length_type == 0:
                sub_length -= self.children[-1].get_length()
            else:
                sub_length -= 1
        self.end_pos = self.children[-1].end_pos

    def unpack_literal(self):
        # literals are a series of 5 bit chunks. If a chunk starts with 1, it's not the last
        # if it starts with zero, it is the last. This function will return the remaining binary
        # representation if there's any left
        literal_rep = ''
        # print('literal packet is', self.binary_rep[self.start_pos:])
        ptr = self.start_pos + 6
        while self.binary_rep[ptr] == '1':
            ptr += 1
            literal_rep += self.binary_rep[ptr:ptr+4]
            ptr += 4
        # one last time...
        literal_rep += self.binary_rep[ptr+1:ptr+5]
        self.literal_value = int(literal_rep, 2)
        # print('found literal value of', self.literal_value)
        self.end_pos = ptr + 4

    def get_recursive_version_sum(self):
        return self.version + sum([x.get_recursive_version_sum() for x in self.children])

def get_data(is_test=True):
    path = 'inputs/day16.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()

    bin_reps = []
    for line in lines:
        hex_rep = line.strip()
        bin_reps.append(bin(int(hex_rep, 16))[2:].zfill(len(hex_rep) * 4))
    return bin_reps

@aoc_utils.timer
def part1(data):
    for d in data:
        p = Packet(d, 0)
        print('Part 1:', p.get_recursive_version_sum())

@aoc_utils.timer
def part2(data):
    for d in data:
        p = Packet(d, 0)
        print('Part 2:', p.get_value())

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    data = get_data(is_test)
    part1(data)
    part2(data)
