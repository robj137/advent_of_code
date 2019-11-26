import json
import datetime as dt
import re
from collections import defaultdict
import heapq

class State:
    """Encapsulate the snapshot of what's where."""
    def __init__(self, floor_dict, elevator_loc=1, counter=0):
        self.floors = {}
        self.counter = counter
        self.elevator_loc = elevator_loc
        for key in floor_dict:
            self.floors[key] = floor_dict[key][:]
        self.sort()
        
    # overload comparison operators! then use heapq's natural ordering 

    def __gt__(self, other):
        return self.counter + self.floor_score > other.counter + self.floor_score
    
    def __lt__(self, other):
        return self.counter + self.floor_score < other.counter + self.floor_score
    
    def __ge__(self, other):
        return self.counter + self.floor_score >= other.counter + self.floor_score
    
    def __le__(self, other):
        return self.counter + self.floor_score <= other.counter + self.floor_score
    
    def __eq__(self, other):
        # the floors and the elevator have to be the same
        if self.elevator_loc != other.elevator_loc:
            return False
        if self.floors != other.floors:
            return False
        return True

    def __hash__(self):
        return hash(self.string_rep)

    def get_copy(self):
        d = {1:[], 2:[], 3:[], 4:[]}
        for i in [1,2,3,4]:
            d[i] = self.floors[i][:]
        return d

    def sort(self):
        score = 0
        for floor in self.floors:
            self.floors[floor].sort()
            score += 16**(4-floor) * len(self.floors[floor])
        self.floor_score = score
        self.string_rep = self.stringify()
    
    def add_object_to_floor(self, obj_type, floor):
        self.floors[floor].append(obj_type)

    def remove_object_from_floor(self, obj_type, floor):
        if obj_type in self.floors[floor]:
            self.floors[floor].pop(self.floors[floor].index(obj_type))

    def move_object_between_floors(self, obj_type, floor_1, floor_2):
        if obj_type == None:
            return
        self.remove_object_from_floor(obj_type, floor_1)
        self.add_object_to_floor(obj_type, floor_2)

    def is_finished(self):
        for floor in [1,2,3]:
            if self.floors[floor]:
                return False
        return True

    def get_counter(self):
        return self.counter

    def stringify(self):
        s = json.dumps(self.floors)
        return json.dumps(self.floors) + '-' + str(self.elevator_loc)

    def print(self):
        for floor in self.floors:
            print(floor, self.floors[floor])

    def get_candidates(self):
        # basically, find where the elevator is and return that floor
        floor_contents = self.floors[self.elevator_loc][:]
        floor_contents.append(None)
        return floor_contents


    def check_elevator_ride(self, o1, o2):
        return True
        if (o1 and not o2) or (o2 and not o1):
            # only one item, we're good
            return True
        n_generators = sum(['G-' in x for x in [o1, o2]]) 
        n_chips = sum(['M-' in x for x in [o1, o2]]) 
        # check if elevator ride is ok
        if n_generators == 1 and n_chips == 1:
            if o1.split('-')[1] != o2.split('-')[1]:
                return False
        return True

    def check_objs(self, objs):
        # make sure nothing is getting fried.
        chips = []
        generators = []
        for o in objs:
            if 'M-' in o:
                chips.append(o.split('-')[1])
            else:
                generators.append(o.split('-')[1])
        if len(generators) == 0:
            # no generators, everything is fine
            return True
        for chip in chips:
            if chip not in generators:
               # there is no generator for this chip, so not allowd
                return False
        return True

    def check_new_floor(self, floor, o1, o2):
        new_floor = self.floors[floor][:]
        [new_floor.append(x) for x in [o1, o2] if x]
        return self.check_objs(new_floor) 

    def check_old_floor(self, floor, o1, o2):
        old_floor = self.floors[floor][:]
        for o in [o1, o2]:
            if o in old_floor:
                old_floor.pop(old_floor.index(o))
        return self.check_objs(old_floor)


    def check_is_allowed(self, floor_1, floor_2, o1, o2):
        # check if elevator and objecs are on floor_1
        if o1 and o1 not in self.floors[floor_1]:
            return False
        # need at least one object to move
        if not o1 and not o2:
            return False
        # can only move one floor at a time
        if abs(floor_1 - floor_2) != 1:
            return False
        if not self.check_elevator_ride(o1, o2):
            return False
        
        if not self.check_new_floor(floor_2, o1, o2):
            return False

        if not self.check_old_floor(floor_1, o1, o2):
            return False

        return True


def get_inputs(test=False):
    path = 'inputs/day11.txt'
    if test:
        path = 'inputs/day11.test.txt'
    with open(path) as f:
        lines = [x.strip() for x in f.readlines()]
    
    floor_map = {'first':1, 'second':2, 'third':3, 'fourth':4}
    d = {u:[] for u in floor_map.values()}
    objs = []
    for line in lines:
        if 'nothing relevant' in line:
            continue
        floor = floor_map[line.split(' ')[1]]
        items = line.split('contains ')[1]
        for part in items.split('and'):
            for obj in part.split(','):
                o = obj.strip()
                if ' ' in o:
                    typ = o.split(' ')[-1][0].upper()
                    element = o.split(' ')[1][0:2].capitalize()
                    obj_to_add = '{}-{}'.format(typ, element)
                    objs.append(obj_to_add)
                    d[floor].append(obj_to_add)
    
    state = State(d, 1, 0)
    return state, objs

def get_neighbors(state):
    elevator_loc = state.elevator_loc
    candidate_floors = [x for x in [elevator_loc - 1, elevator_loc + 1] if x > 0 and x < 5]
    #candidate_

def process_state(queue, visited, state, finished):
    if state.is_finished():
        heapq.heappush(finished, state.get_counter())
        return
    if state.get_counter() > finished[0]:
        return
    visited[state] = state.get_counter()
    candidates = state.get_candidates()
    floor_options = [x for x in [state.elevator_loc-1, state.elevator_loc+1] if x > 0 and x < 5]
    while candidates:
        o1 = candidates.pop()
        for o2 in candidates:
            for new_floor in floor_options:
                if state.check_is_allowed(state.elevator_loc, new_floor, o1, o2):
                    new_state = State(state.get_copy(), new_floor, state.get_counter() + 1)
                    new_state.move_object_between_floors(o1, state.elevator_loc, new_floor)
                    new_state.move_object_between_floors(o2, state.elevator_loc, new_floor)
                    new_state.sort()
                    if new_state not in visited and new_state.get_counter() < finished[0]:
                        visited[new_state] = new_state.get_counter()
                        heapq.heappush(queue, new_state)
                    elif new_state in visited:
                        if new_state.get_counter() < visited[new_state]:
                            visited[new_state] = new_state.get_counter()
                            heapq.heappush(queue, new_state)


def do_part(initial_state):
    initial_state.sort()

    visited_states = defaultdict(int)
    visited_states['zomg'] = 0
    queue = []
    heapq.heappush(queue, initial_state)
    finished = []
    heapq.heappush(finished, 100)
    while queue:
        #print('queue length is', len(queue), 'visited length is', len(visited_states))
        new_state = heapq.heappop(queue)
        if new_state.get_counter() < finished[0]:
            process_state(queue, visited_states, new_state, finished)
    return finished

def part2():
    initial_state, objs = get_inputs(False)
    initial_state.add_object_to_floor('El-M', 1)
    initial_state.add_object_to_floor('El-G', 1)
    initial_state.add_object_to_floor('Di-M', 1)
    initial_state.add_object_to_floor('Di-G', 1)
    initial_state.sort()
    finished = do_part(initial_state)
    print('Part 2: Least amount of steps to bring everything to 4th floor is {}'.format(min(finished)))   

def part1():
    initial_state, objs = get_inputs(False)
    finished = do_part(initial_state)
    print('Part 1: Least amount of steps to bring everything to 4th floor is {}'.format(min(finished)))   
    #print(visited_states)

def main():
    part1()
    part2()


if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
