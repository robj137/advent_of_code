import numpy as np
import re

def get_initial_state(state_input):
    """Parse the input lines corresponding to the initial crate state.

    Have already separated the "state" bit from the instructions. Here
    we just convert each string line into an array of characters, then
    convert it to a numpy array, transpose it, and throw awahy the rows
    that aren't the crate identifiers. Reverse the arrays and we're left
    with stacks of crates.
    """
    state_input = np.array([list(x) for x in state_input]).T
    state_input = np.array(
        [x for x in state_input if x[-1] not in [']', '[', ' ']]
    )
    state_input = [''.join(x).strip()[::-1] for x in state_input]
    return [list(x) for x in state_input]

def get_instructions(instructs):
    """Use RegEx to convert the instructions to useful integer.s"""
    instructions = []
    pat = 'move (\d+) from (\d+) to (\d+)'
    for line in instructs:
        instructions.append([int(x) for x in re.search(pat, line).groups()])
    return instructions

def get_initial_state_and_instructions(lines):
    """Find the blank line, split the input on that, and let's rock."""
    blank_line = lines.index('')
    return (
        get_initial_state(lines[:blank_line]),
        get_instructions(lines[blank_line + 1:])
    )

def rearrange(state, instructions, ordering=1):
    """Use index magic to move crates from one pile to the next."""
    for n_crates, from_crate, to_crate in instructions:
        state[to_crate - 1].extend(
        [state[from_crate - 1].pop() for x in range(n_crates)][::ordering]
    )
    return ''.join([x.pop() for x in state])

if __name__ == '__main__':
    #with open('inputs/day05.test.txt') as f:
    with open('inputs/day05.txt') as f:
        lines = [x.strip('\n') for x in f.readlines()]
    
    state, instructions = get_initial_state_and_instructions(lines)
    top_of_stack = rearrange(state, instructions, 1)
    print('part 1:', top_of_stack)
    
    state, instructions = get_initial_state_and_instructions(lines)
    top_of_stack = rearrange(state, instructions, -1)
    print('part 2:', top_of_stack)
