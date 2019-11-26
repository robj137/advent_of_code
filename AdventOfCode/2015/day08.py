import re
import numpy as np


def get_decoded_string_totals(s):
    n_chars_s_l = len(s)
    extra_slash_count = 0
    extra_quote_count = 0
    while '\\\\' in s:
        extra_slash_count += 1
        s = s.replace('\\\\', '', 1)
    while '\\"' in s:
        extra_quote_count += 1
        s = s.replace('\\"', '', 1)
    pattern = '(\\\\x[a-z0-9][a-z0-9])' 
    n_hex_chars = len(re.findall(pattern, s))
    n_chars_s_v = n_chars_s_l - 2 - extra_slash_count - extra_quote_count - 3 * n_hex_chars
    n_chars_e = n_chars_s_l + 4 + 2 * extra_slash_count + 2 * extra_quote_count + n_hex_chars
    return n_chars_s_l, n_chars_s_v, n_chars_e

def main():
    with open('inputs/day8_alt.txt') as f:
    #with open('inputs/day8.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    n_chars_string_literals = []
    n_chars_values = []
    n_chars_encoded = []
    for line in lines:
        a, b, c = get_decoded_string_totals(line)
        n_chars_string_literals.append(a)
        n_chars_values.append(b)
        n_chars_encoded.append(c)
    n_chars_s_l = sum(n_chars_string_literals)
    n_chars_v = sum(n_chars_values)
    n_chars_e = sum(n_chars_encoded)
    n_chars_diff1 = n_chars_s_l - n_chars_v
    n_chars_diff2 = n_chars_e - n_chars_s_l
    msg = 'Sum of number of characters of code for string literals: {}\n'
    msg += 'Sum of number of characters in memory for string values: {}\n'
    msg += 'Sum of number of encoded characters: {}\n'
    msg += 'Part 1: Difference 1: {}\n'
    msg += 'Part 2: Difference 2: {}\n'
    msg = msg.format(n_chars_s_l,
                     n_chars_v,
                     n_chars_e,
                     n_chars_diff1,
                     n_chars_diff2)
    print(msg)
if __name__ == '__main__':
  main()

