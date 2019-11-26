import numpy as np
import datetime as dt
from collections import deque, Counter


class Packet:
    def __init__(self, pos: complex, di: complex):
        self.position = pos
        self.direction = di
        self.letters = ''
        self.steps = 0

def get_start(track):
  found = False
  pos = 0 + 0j
  direction = 1 + 0j
  start = 0
  while not found:
    if direction.real: #going up down, look for '-'
      segment = '-'
    else: #going up down, looking for '|'
      segment = '|'
    if track[(int(pos.real), int(pos.imag))] == segment:
      start = pos
      found = True
    else: pos += direction
    if not check_inbounds(pos, track):
      pos -= direction # need to back up and make a turn
      direction *= 1j
  return start

def take_step(packet, track):
  packet.steps += 1
  previous_step = track[get_coord(packet.position)]
  packet.position += packet.direction
  line = track[get_coord(packet.position)]
  if line in '|-':
    return
  if line == '+':
    packet.direction *= -1j
    next_step = packet.position + packet.direction
    if not check_inbounds(next_step, track):
      packet.direction *= -1
      next_step = packet.position + packet.direction
    next_step = track[get_coord(next_step)]
    if next_step == previous_step or next_step == ' ':
      packet.direction *= -1 # took a wrong turn :) and this assumes there are no 'u-turns', i.e. ++ horiz or vert
    return
  else:
    packet.letters += line

def get_coord(pos):
  return int(pos.real), int(pos.imag)

def check_inbounds(pos, track):  
  return not (pos.real < 0 or pos.imag < 0 or pos.real >= track.shape[0] or pos.imag >= track.shape[1])

def main():
  tracks = []
  with open('inputs/day19.txt') as f:
    for line in f:
      tracks.append((list(line.strip('\n'))))

  track = np.array(tracks)
  
  start = get_start(track)
  direction = start / np.abs(start) / 1j
  packet = Packet(start, direction)
  print(get_coord(start),  dir, track[get_coord(start)])

  while ' ' not in packet.letters:
    take_step(packet, track)

  print('Part a: the letters the packet picks up along the way are {}'.format(packet.letters))
  print('Part b: the amount of steps to get there was {}'.format(packet.steps))

if __name__ == '__main__':
  begin = dt.datetime.now()
  main()
  diff_time = dt.datetime.now() - begin
  print('That took {:.3f} seconds'.format(diff_time.seconds + 1e-6*diff_time.microseconds))

