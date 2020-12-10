import datetime as dt
from collections import Counter
from datetime import datetime as dt
import numpy as np


class Passport:
    def __init__(self, lines):
        self.fields = {}
        self.field_names = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
        self.fields['byr'] = None
        self.fields['iyr'] = None
        self.fields['eyr'] = None
        self.fields['hgt'] = None
        self.fields['hcl'] = None
        self.fields['ecl'] = None
        self.fields['pid'] = None
        self.fields['cid'] = 'Temp'
        for line in lines:
            for pair in line.strip().split(' '):
                field, val = pair.split(':')
                self.fields[field] = val

        self.valid_items = 0
        self.check_is_valid()

        

    def number_check(self, val, lo, hi):
        val = int(val)
        if val < lo or val > hi:
            return False
        return True
    
    def check_is_valid(self):
        self.is_valid = True
        for field in self.fields:
            if self.fields[field] is None:
                self.is_valid = False
                return
            val = self.fields[field]
            if field == 'byr':
                if not  self.number_check(val, 1920, 2002):
                    self.is_valid = False
                    return
            if field == 'iyr':
                if not self.number_check(val, 2010, 2020):
                    self.is_valid = False
                    return
            if field == 'eyr':
                if not self.number_check(val, 2020, 2030):
                    self.is_valid = False
                    return
            if field == 'hgt':
                units = val[-2:]
                val = val[0:-2]
                if units == 'cm':
                    if not self.number_check(val, 150, 193):
                        self.is_valid = False
                        return
                elif units == 'in':
                    if not self.number_check(val, 59, 76):
                        self.is_valid = False
                        return
                else:
                    self.is_valid = False
                    return
            if field == 'hcl':
                if val[0] != '#' or len(val) != 7:
                    self.is_valid = False
                    return
                try:
                    _ = int(val[1:], 16)
                except Exception as e:
                    self.is_valid = False
                    return
            if field == 'ecl':
                if val not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    self.is_valid = False
                    return
            if field == 'pid':
                if len(val) != 9:
                    self.is_valid = False
                    return
                try:
                    _ = int(val)
                except Exception as e:
                    self.is_valid = False
                    return

        return

def get_data(is_test=False):
    if is_test:
        in_file = 'inputs/day04.test.txt'
    else:
        in_file = 'inputs/day04.txt'
    
    with open(in_file) as f:
        lines = [x.strip() for x in f.readlines()]
 
    passports = []
    batch = []
    for line in lines:
        if len(line) < 2:
            if len(batch) > 0:
                passports.append(Passport(batch))
            batch = []
        else:
            batch.append(line.strip())

    if len(batch) > 0:
        passports.append(Passport(batch))

    n_valid = 0
    for p in passports:
        if p.is_valid:
            n_valid += 1
    print(n_valid)
    return passports

def main():
    data = get_data(is_test=False)
    print(len(data))

if __name__ == '__main__':
    begin = dt.now()
    main()
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
