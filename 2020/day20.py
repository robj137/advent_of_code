import heapq
import datetime as dt
from collections import Counter, defaultdict
from datetime import datetime as dt
import numpy as np
import re


class Tile:
    def __init__(self, tile_number, lines):
        self.__number__ = tile_number
        self.og_content = np.array([ np.fromiter(x.strip(), (np.unicode,1)) for x in lines])
        self.current_content = self.og_content.copy()
        self.side_candidates = None
        self.possible_matches = dict()
        self.grid_loc = None # where it will sit in the picture grid
        self.rotation = 0
        self.parity = 0
        self.to_match_side_direction = None # will be 'top', 'left', 'bottom', or 'right'
        self.to_match_side = None # will be a string 

        self.picture_content = None

    def rotate(self):
        self.current_content = np.rot90(self.current_content)

    def flip(self, axis=1):
        self.current_content = np.flip(self.current_content, axis=axis)

    def orient(self):
        rotations = 0
        while self.get_side(self.to_match_side_direction) != self.to_match_side:
            if rotations == 4:
                # flip once after going through four rotations to get mirrored-version
                self.flip(axis=1)
            self.rotate()
            rotations += 1        
            if rotations > 9:
                print('something went wrong and could not orient tile', self.__number__)
                print(self.og_content)
                print('to match side', self.to_match_side_direction, 'with', self.to_match_side)
                break


    def print_map(self, kind='current'):
        content = self.current_content if kind=='current' else self.og_content
        lines = [''.join(x) for x in content]
        for l in lines:
            print(l)

    def get_side(self, side):
        rep = ''
        m = self.current_content
        if side == 'top':
            rep = ''.join(m[0, :])
        elif side == 'right':
            rep = ''.join(m[:, -1])
        elif side == 'bottom':
            rep = ''.join(m[-1, :])
        elif side == 'left':
            rep = ''.join(m[:, 0])
        return rep

    def get_side_candidates(self):
        if not self.side_candidates:
            temp = self.og_content.copy()
            self.side_candidates = {}
            rot = 0
            parity = 0
            for i in range(4):
                temp = np.rot90(temp)
                rot = (rot + 90) % 360
                parity = 0
                label = (rot, parity)
                self.side_candidates[''.join(temp[0])] = label
                parity = 1
                label = (rot, parity)
                self.side_candidates[''.join(temp[0][::-1])] = label
        return self.side_candidates


class Picture:
    def __init__(self, is_test=True):
        self.is_test = is_test
        self.corner_pieces = []
        self.get_data()
        self.placed = {}
        self.to_place = [] # heapq: after a tile gets placed, push it here
        self.find_possible_neighbors()
        self.get_monster_pic()
    
    def print_picture(self, kind='monster'):
        pic = self.final_picture
        if kind == 'pristine':
            pic = self.final_picture.copy()
            pic[pic == '█'] = '#'
        pic[pic== '.'] = ' '
        lines = [''.join(x) for x in pic]
        for l in lines:
            print(l)

    def part1(self):
        for tile_number in self.tiles:
            tile = self.tiles[tile_number]
            if len(tile.possible_matches) == 2:
                self.corner_pieces.append(tile_number)

    def run(self):
        self.part1()
        self.place_tile(None, (0, 0))
        self.build_picture()
        self.check_for_monsters()
        self.water_roughness = self.n_picture_hashes - self.number_of_monsters * self.n_monster_hashes


    def get_data(self):
        if self.is_test:
            in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day20.test.txt'
        else:
            in_file = '/Users/rob/Code/advent_of_code/2020/inputs/day20.txt'
    
        with open(in_file) as f:
            lines = [x.strip() for x in f.readlines()]
    
        tiles = {}
        tile_reader = re.compile('^Tile (\d+):$')
        while lines:
            tile_lines = lines[0:12]
            lines = lines[12:]
            tile_number = int(tile_reader.search(tile_lines[0]).groups()[0])
            tile = Tile(tile_number, tile_lines[1:11])
            tiles[tile_number] = tile

        for tile_number in tiles:
            tile = tiles[tile_number]
        self.tiles = tiles


    def get_monster_pic(self):
        monster_file = '/Users/rob/Code/advent_of_code/2020/inputs/day20.monster.txt'
        with open(monster_file) as f:
            lines = [x.strip() for x in f.readlines()]
        self.monster_pic = np.array([ np.fromiter(x.strip(), (np.unicode,1)) for x in lines])
        self.n_monster_hashes = np.sum(self.monster_pic == '#')

    def build_picture(self):
        loc_pic_dict = {self.placed[x]: self.tiles[x].picture_content for x in self.placed}
        n_tiles = int(len(loc_pic_dict)**0.5)
        rows = []
        for y in range(n_tiles):
            cols = []
            for x in range(n_tiles):
                cols.append(loc_pic_dict[(x,y)])
            rows.insert(0, np.concatenate(cols, axis=1))
        self.final_picture = np.concatenate(rows, axis=0)
        self.n_picture_hashes = np.sum(self.final_picture == '#')

    def check_for_monsters(self):
        monster_shape = self.monster_pic.shape
        picture_shape = self.final_picture.shape
        monsters_found = 0
        monster_mesh = (self.monster_pic == '#')
        rotations = 0
        while monsters_found == 0:
            self.final_picture = np.rot90(self.final_picture)
            if rotations == 8:
                print('uh oh, where the monster at?')
            if rotations == 4:
                # didn't find any, so let's flip the script
                self.final_picture = np.fliplr(self.final_picture)
            for y in range(0, 1 + picture_shape[0] - monster_shape[0]):
                for x in range(0, 1 + picture_shape[1] - monster_shape[1]):
                    area = self.final_picture[y:y + monster_shape[0], x:x + monster_shape[1]]
                    area_mesh = (area == '#')
                    if np.all(np.logical_and(area_mesh, monster_mesh) == monster_mesh):
                        area[monster_mesh] = '█'
                        monsters_found += 1
            rotations += 1
        self.number_of_monsters = monsters_found


    def find_possible_neighbors(self):
        tile_numbers = [x for x in self.tiles]
        for i in range(len(tile_numbers)):
            tile_i = self.tiles[tile_numbers[i]]
            sides_i = tile_i.get_side_candidates()
            for j in range(i+1, len(tile_numbers)):
                tile_j = self.tiles[tile_numbers[j]]
                sides_j = tile_j.get_side_candidates()
                for side_i in sides_i:
                    if side_i in sides_j:
                        tile_i.possible_matches[tile_numbers[j]] = side_i
                        tile_j.possible_matches[tile_numbers[i]] = side_i

    def bootstrap_first_tile(self):
        keys = self.tiles.keys()
        corner = None
        for key in keys:
            if len(self.tiles[key].possible_matches) == 2:
                corner = self.tiles[key]

        # first let's orient the corner so the side to the right is a possible match
        keys = [x for x in corner.possible_matches.keys()]
        first_key = keys[0]
        second_key = keys[1]
        corner.to_match_side_direction = 'right'
        corner.to_match_side = corner.possible_matches[first_key]
        corner.orient()
        # now check if the other corner is on the top or not.
        second_side = corner.possible_matches[second_key]
        second_side_options = [second_side, second_side[::-1]]
        if corner.get_side('top') not in second_side_options:
            corner.flip(axis=0)
        return corner

    def place_tile(self, tile, loc):
        if loc == (0, 0): #it's the first tile placed, so find the corner
            tile = self.bootstrap_first_tile()
        else:
            # not the first tile, so the tile already knows which side to match and how
            tile.orient()

        # now to
        # - go through this tile's matches and for each match
        # - figure out the location of the new tile
        # - set the corresponding matched side and matched side direction
        # - add it to the priority queue

        new_loc = None
        for match in tile.possible_matches:
            match_side = tile.possible_matches[match]
            match_side_options = [match_side, match_side[::-1]]
            # by constructions, we're building this from the bottom to the top
            # and the left to the right. 
            if tile.get_side('top') in match_side_options:
                    new_loc = np.array(loc) + (0, 1)
                    matching_side_direction = 'bottom'
                    match_side = tile.get_side('top')
            elif tile.get_side('right') in match_side_options:
                    new_loc = np.array(loc) + (1, 0)
                    matching_side_direction = 'left'
                    match_side = tile.get_side('right')
            elif tile.get_side('bottom') in match_side_options:
                    new_loc = np.array(loc) + (0, -1)
                    matching_side_direction = 'top'
                    match_side = tile.get_side('bottom')
            elif tile.get_side('left') in match_side_options:
                    new_loc = np.array(loc) + (-1, 0)
                    matching_side_direction = 'right'
                    match_side = tile.get_side('left')
            else:
                continue
            self.tiles[match].to_match_side = match_side
            self.tiles[match].to_match_side_direction = matching_side_direction
            to_add = (tuple(new_loc), match)
            if match not in self.placed and to_add not in self.to_place:
                heapq.heappush(self.to_place, to_add)
        self.placed[tile.__number__] = loc
        tile.picture_content = tile.current_content[1:-1,1:-1]


        if self.to_place:
            new_loc, new_tile_key = heapq.heappop(self.to_place)
            new_tile = self.tiles[new_tile_key]
            self.place_tile(new_tile, new_loc)


if __name__ == '__main__':
    begin = dt.now()
    is_test = False
    picture = Picture(is_test)
    picture.run()   
    print('Part 1:', np.prod(picture.corner_pieces))
    print('Part 2: Water Roughness is {}'.format(picture.water_roughness))
    diff_time = dt.now() - begin
    print('That took {:.6f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))
