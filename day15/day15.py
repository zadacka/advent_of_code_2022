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


def test__load_sensors():
    expected = {(0, 11): (2, 10),
                (10, 20): (10, 16),
                (12, 14): (10, 16),
                (13, 2): (15, 3),
                (14, 17): (10, 16),
                (14, 3): (15, 3),
                (16, 7): (15, 3),
                (17, 20): (21, 22),
                (2, 0): (2, 10),
                (2, 18): (-2, 15),
                (20, 1): (15, 3),
                (20, 14): (25, 17),
                (8, 7): (2, 10),
                (9, 16): (10, 16)}
    assert expected == load_sensors('day15_test_input.txt')


def test__sensor_coverage():
    assert {(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)} == sensor_coverage((0, 0), (0, 1))


def sensor_coverage(sensor, beacon):
    s_x, s_y = sensor
    b_x, b_y = beacon
    coverage = set()
    sensor_beacon_taxicab_distance = max(s_y, b_y) - min(s_y, b_y) + max(s_x, b_x) - min(s_x, b_x)
    for x in range(s_x - sensor_beacon_taxicab_distance, s_x + sensor_beacon_taxicab_distance + 1):
        for y in range(s_y - sensor_beacon_taxicab_distance, s_y + sensor_beacon_taxicab_distance + 1):
            sensor_point_taxicab_distance = max(s_y, y) - min(s_y, y) + max(s_x, x) - min(s_x, x)
            if sensor_point_taxicab_distance <= sensor_beacon_taxicab_distance:
                coverage.add((x, y))
    return coverage


def find_blank_spots(input_filename, row):
    sensor_beacon_map = load_sensors(input_filename)
    min_x = min(min(key[0], value[0]) for key, value in sensor_beacon_map.items())
    max_x = max(max(key[0], value[0]) for key, value in sensor_beacon_map.items())
    # min_y = min(min(key[1], value[1]) for key, value in sensor_beacon_map.items())
    # max_y = max(max(key[1], value[1]) for key, value in sensor_beacon_map.items())
    coverage = set()
    for sensor, beacon in sensor_beacon_map.items():
        coverage.update(sensor_coverage(sensor, beacon))
    well_covered = 0
    for x in range(min_x, max_x + 1):
        if (x, row) in coverage and not (x, row) in sensor_beacon_map.values():
            well_covered += 1
    return well_covered


def test_find_blank_spots():
    assert 26 == find_blank_spots('day15_test_input.txt', 10)

def test_part1():
    assert 26 == find_blank_spots('day15_real_input.txt',2000000)