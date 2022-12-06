import numpy as np
import re
import sys
import json
from collections import Counter, defaultdict
from scipy.spatial.transform import Rotation as R



class Sensor:
    def __init__(self, label, beacons):
        self.label = label
        self.beacons = beacons.copy()
        self.diffs = self.get_differences()
    def get_differences(self):
        diffs = defaultdict(list)
        for i in range(0, len(self.beacons)):
            for j in range(i+1, len(self.beacons)):
                beacon1 = self.beacons[i]
                beacon2 = self.beacons[j]
                diffs[np.linalg.norm(beacon1 - beacon2)].append((beacon1, beacon2))
        return diffs
    def apply_shift(self, vec):
        self.beacons = [x + vec for x in self.beacons]
    def apply_pi_over_2_rotation(self, rot_axis):
        rotation_vector = np.radians(90) * rot_axis
        rotation = R.from_rotvec(rotation_vector)
        self.beacons = [rotation.apply(x) for x in self.beacons]

class Cluster:
    def __init__(self, sensor_dict):
        self.unmatched = [x for x in sensor_dict]
        self.sensor_dict = sensor_dict
        self.set_initial_beacons(self.unmatched[0], self.sensor_dict[self.unmatched[0]].beacons)
    def set_initial_beacons(self, label, beacons):
        self.beacons = beacons.copy()
        if label in self.unmatched:
            self.unmatched.pop(self.unmatched.index(label))
        self.diffs = self.get_differences(self.beacons)
    def get_differences(self, beacons):
        diffs = defaultdict(list)
        for i in range(0, len(beacons)):
            for j in range(i+1, len(beacons)):
                beacon1 = beacons[i]
                beacon2 = beacons[j]

                diffs[np.linalg.norm(beacon1 - beacon2)].append((beacon1, beacon2))
        return diffs

    def set_trial_sensor(self, label, beacons):
        self.trial_beacons = beacons.copy()
        self.trial_diffs = self.get_differences(beacons)

    def attempt_to_match(self):
        matched_diffs = set(self.diffs).intersection(set(self.trial_diffs))
        if len(matched_diffs) < 66:
            return False # not enough matches
        v1 = []
        v2 = []
        for match in matched_diffs:
            # what if more than ome match? FIXME
            trusted_a, trusted_b = self.diffs[match][0]
            v1.append(trusted_a - trusted_b)
            trial_a, trial_b = self.trial_diffs[match][0]
            v2.append(trial_a - trial_b)
        return v1, v2


def get_data(is_test=True):
    path = 'inputs/day19.txt'
    path = path.replace('.txt', '.test.txt') if is_test else path
    with open(path) as f:
        lines = f.readlines()

    sensor_pattern = '--- scanner (\d+) ---'
    coord_pattern = '(-?\d+),(-?\d+),(-?\d+)'
    sensors = defaultdict(list)
    current_sensor = None
    for line in lines:
        sensor_try = re.search(sensor_pattern, line)
        coord_try = re.search(coord_pattern, line)
        if sensor_try:
            current_sensor = int(sensor_try.groups()[0])
        elif coord_try:
            coord = np.array([int(x) for x in coord_try.groups()])
            sensors[current_sensor].append(coord)
    
    sensor_dict = {}
    for s in sensors:
        label = s
        beacons = sensors[s]
        sensor_dict[label] = Sensor(label, beacons)

    return sensor_dict

if __name__ == '__main__':
    is_test = True if len(sys.argv) > 1 and sys.argv[1] == 'test' else False
    sensors = get_data(is_test)
    print(sensors)
    cluster = Cluster(sensors)
