def load_sensors(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    result = dict()
    for line in lines:
        sensor, beacon = line.split(':')
        sensor_tokens = sensor.split()
        sensor_x = int(sensor_tokens[-2].split('=')[1].replace(',', ''))
        sensor_y = int(sensor_tokens[-1].split('=')[1])
        beacon_tokens = beacon.split()
        beacon_x = int(beacon_tokens[-2].split('=')[1].replace(',', ''))
        beacon_y = int(beacon_tokens[-1].split('=')[1])
        result[(sensor_x, sensor_y)] = (beacon_x, beacon_y)
    return result


def manhattan_distance(sensor, beacon):
    s_x, s_y = sensor
    b_x, b_y = beacon
    coverage = set()
    return max(s_y, b_y) - min(s_y, b_y) + max(s_x, b_x) - min(s_x, b_x)


def no_beacon_places(input_filename, y):
    sensor_beacon_map = load_sensors(input_filename)
    min_x = min(min(key[0], value[0]) for key, value in sensor_beacon_map.items())
    max_x = max(max(key[0], value[0]) for key, value in sensor_beacon_map.items())

    coverage = set()
    # NO!!! mix_x and max_x can be different from this - they are the maximal *scan* distances, not the grid by where scanners/beacons are
    for x in range(min_x, max_x + 1):
        for sensor, beacon in sensor_beacon_map.items():
            if manhattan_distance(sensor, (x, y)) <= manhattan_distance(sensor, beacon):
                coverage.add((x, y))
                break  # know this is covered no need to find other regions that hit it
    beacons = set(b for b in sensor_beacon_map.values())
    sensors = set(b for b in sensor_beacon_map.keys())
    return len(coverage - beacons - sensors)


def test_find_blank_spots():
    assert 26 == no_beacon_places('day15_test_input.txt', 10)


def test_part1():
    assert 26 == no_beacon_places('day15_real_input.txt', 2000000)
