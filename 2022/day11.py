import numpy as np

def get_data():
    with open('inputs/day11.txt') as f:
    #with open('inputs/day11.test.txt') as f:
        monkeys = [x for x in f.read().split('\n\n')]
    return [x.split('\n') for x in monkeys]

class Monkey:
    def __init__(self, blurb, worry=False):
        self.worry = worry
        self.troop = None
        self.parse_monkey_blurb(blurb)
        self.inspections = 0
        self.grand_divisor = 1

    def parse_monkey_blurb(self, blurb):
        self.n = int(blurb[0].split()[-1][0])
        self.items = [int(x.strip()) for x in blurb[1].split(':')[-1].split(',')]
        self.operation = self.get_operation_lambda(blurb[2])
        self.true_tgt = int(blurb[4].split()[-1])
        self.false_tgt = int(blurb[5].split()[-1])
        self.test_divisor = int(blurb[3].split()[-1])
        self.set_test(self.test_divisor, self.true_tgt, self.false_tgt)

    def set_troop(self, troop):
        # dictionary / array of all monkeys
        self.troop = troop

    def set_grand_divisor(self, divisor):
        self.grand_divisor = divisor

    def set_test(self, div_n, true_tgt, false_tgt):
        self.target = lambda x: self.troop[true_tgt] if x%div_n == 0 else self.troop[false_tgt]

    def catch_item(self, item):
        self.items.append(item)

    def play_with_item(self):
        self.inspections += 1
        item = self.items.pop()
        item = self.operation(item)
        item = item % self.grand_divisor
        item = item // 3 if not self.worry else item
        target_monkey = self.target(item)
        target_monkey.items.append(item)

    def do_turn(self):
        while self.items:
            self.play_with_item()
        
    def get_operation_lambda(self, line):
        line = line.split('=')[-1]
        if "old * old" in line:
            return lambda x: x**2
        # that takes care of the one case where old is both args
        # now just figure out the operation and the value
        val = int(line.split()[-1])
        if '*' in line:
            return lambda x: x * val
        else:
            return lambda x: x + val

    def print_status(self):
        print("Status for Monkey", self.n, 'with items:', self.items, 'and ', self.inspections, 'inspections')

if __name__ == '__main__':
    data = get_data()
    worry_free_monkeys = [Monkey(blurb, worry=False) for blurb in data]
    worry_full_monkeys = [Monkey(blurb, worry=True) for blurb in data]
    [x.set_troop(worry_free_monkeys) for x in worry_free_monkeys]
    [x.set_troop(worry_full_monkeys) for x in worry_full_monkeys]
    grand_divisor = np.prod([x.test_divisor for x in worry_full_monkeys])
    [x.set_grand_divisor(grand_divisor) for x in worry_full_monkeys]
    for i in range(20):
        [x.do_turn() for x in worry_free_monkeys]
    inspections = [x.inspections for x in worry_free_monkeys]
    inspections.sort()
    inspections.reverse()
    print('Part 1:', inspections[0] * inspections[1])
    for i in range(10000):
        [x.do_turn() for x in worry_full_monkeys]
    inspections = [x.inspections for x in worry_full_monkeys]
    inspections.sort()
    inspections.reverse()
    print('Part 2:', inspections[0] * inspections[1])
