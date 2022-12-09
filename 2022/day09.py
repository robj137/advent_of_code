from collections import defaultdict

dir_dict = {'R': 1, 'U': 1j, 'L': -1, 'D': -1j}

def get_data():
    with open('inputs/day09.txt') as f:
    #with open('inputs/day09.test2.txt') as f:
        lines = [x.strip() for x in f.readlines()]
    return [(x.split()[0], int(x.split()[1])) for x in lines]

def get_modulus(x):
    return (x.imag**2 + x.real**2)**0.5


class Node:
    def __init__(self, name, parent=None, rope_length=10):
        self.name = name
        self.parent = parent
        self.child = None
        self.pos = 0 + 0j
        self.pos_dict = defaultdict(int)
        self.pos_dict[self.pos] += 1
        self.history = [self.pos]
        
        child = 1 if name == 'H' else int(name) + 1
        if child:
            if child < rope_length:
                self.child = Node(
                    name=child,
                    parent=self,
                    rope_length=rope_length
                )

    def adjust_pos(self, instruct=None):
        if instruct and self.name == 'H':
            direction, num = instruct
            impulse = dir_dict[direction]
            for i in range(num):
                self.pos += impulse
                self.pos_dict[self.pos] += 1
                self.history.append(self.pos)
                self.child.adjust_pos()
        else:
            self.pos = self.get_new_pos()
            self.pos_dict[self.pos] += 1
            self.history.append(self.pos)
            if self.child:
                self.child.adjust_pos()
            
    def get_new_pos(self):
        diff_mod = get_modulus(self.parent.pos - self.pos)
        if diff_mod < 2:
            return self.pos
        impulses = [1, -1, 1j, -1j]
        if diff_mod != int(diff_mod):
            impulses = [1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]
        for impulse in impulses:
            new_pos = self.pos + impulse
            if get_modulus(new_pos - self.parent.pos) < 2:
                return new_pos
        print("why are we still here?", self.pos, self.parent.pos)

if __name__ == '__main__':
    data = get_data()
    rope_length = 10
    h = Node('H', rope_length=rope_length)

    for x in data:
        h.adjust_pos(x)
    
    node = h
    # get the last knot node
    while node.child:
        node = node.child
   
    print(len(node.pos_dict))
    print(node.history)
    print(len(node.history))
