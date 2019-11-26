import re
from collections import defaultdict
import sys


def get_input():
    instructions = []
    with open('inputs/day7.txt') as f:
        instructions = [x.strip() for x in f.readlines()]
    return instructions

def parse_instruction(line):
    # function is always one or two arguments and an uppercase 
    # operator. arguments are alphanumerical, operators are always uppercase
    # words
    left, right = [x.strip() for x in line.split('->')]
    pattern = '([a-z0-9]*)\s?([A-Z]*)\s?([a-z0-9]*)'
    results = re.search(pattern, left)
    groups = []
    if results:
        groups = results.groups()
    if len(groups) != 3:
        msg = 'Something went wrong. This group({}) from this line ({})'
        msg += ' should have 3 elements'
        msg = msg.format(groups, left)
        print(msg)
        sys.exit()
    op = groups[1]
    args = [x for x in groups[0::2] if x] # create list of arguments (1 or 2)
    value = None 
    if not op: 
        # no argument found, so it's a simple pass through
        # set 'op' to 'EQUALS' and deal with it as a normal instruction
        op = 'EQUALS'
    
    instruction = {
                    'op': op,
                    'args': args,
                    'value': value
                  }
    return right, instruction
    
    
def process_input(instructions):
    instructions_dict = defaultdict(dict)
    for line in instructions:
        key, instruction = parse_instruction(line)
        instructions_dict[key] = instruction
    return instructions_dict

#def ensure_values(instructions_dict):
    
def is_int(val):
    try: 
        int(val)
        return True
    except ValueError:
        return False

def calculate(entry_key, instructions_dict):
    """Make sure there is a valid 'value' for entry."""

    # an entry includes an operation ('op'), one or two arguments 
    # (args = [arg1(, arg2)]), and a value which should just be an integer
    
    # Grab the dictionary entry object
    entry = instructions_dict[entry_key]
    # quick exit if we already have a value
    if entry['value'] != None:
        return
    
    
    # first need to ensure that the arguments are already calculated
    
    # the int values corresponding to the argument array
    arg_values = []
    for arg in entry['args']:
        if is_int(arg):
            # The arg is already in a valid (int or 'int') state
            arg_values.append(int(arg))
        else:
            # not int or string int
            if instructions_dict[arg]['value'] == None:
                calculate(arg, instructions_dict)
            arg_values.append(instructions_dict[arg]['value'])

    # possible oeprators are: (NOT, OR, EQUALS, AND, RSHIFT, LSHIFT
    value = None
    op = entry['op']
    if op == 'NOT':
        value = ~arg_values[0]
    if op == 'OR':
        value = arg_values[0] | arg_values[1]
    if op == 'EQUALS':
        value = arg_values[0]
    if op == 'AND':
        value = arg_values[0] & arg_values[1]
    if op == 'RSHIFT':
        value = arg_values[0] >> arg_values[1]
    if op == 'LSHIFT':
        value = arg_values[0] << arg_values[1]

    value = value % 2**16
    instructions_dict[entry_key]['value'] = value

def reset_wires(instructions_dict):
    for key in instructions_dict.keys():
        instructions_dict[key]['value'] = None

def main():
    instructions = get_input()
    instructions_dict = process_input(instructions)
    
    calculate('a', instructions_dict)
    part_1_value = instructions_dict['a']['value']
    print('Part 1: Value for a is {}\n'.format(part_1_value))

    reset_wires(instructions_dict)
    instructions_dict['b']['args'] = [part_1_value]
    calculate('a', instructions_dict)
    part_2_value = instructions_dict['a']['value']
    print('Part 2: Value for a is {}\n'.format(part_2_value))


if __name__ == '__main__':
    main()
