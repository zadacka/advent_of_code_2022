from collections import deque

TEST_HEIGHT_MAP = [
    ['S', 'a', 'b', 'q', 'p', 'o', 'n', 'm'],
    ['a', 'b', 'c', 'r', 'y', 'x', 'x', 'l'],
    ['a', 'c', 'c', 's', 'z', 'E', 'x', 'k'],
    ['a', 'c', 'c', 't', 'u', 'v', 'w', 'j'],
    ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i']
]


def load_map(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    return [[character for character in string.strip()] for string in lines]


def find_target(heightmap, target='S'):
    for row, line in enumerate(heightmap):
        for column, item in enumerate(line):
            if item == target:
                return column, row
    raise RuntimeError('Target {} Cell not found.'.format(target))


def test__load_map():
    assert TEST_HEIGHT_MAP == load_map('day12_test_input.txt')


def test__find_start():
    assert (0, 0) == find_target(TEST_HEIGHT_MAP, target='S')


def is_reachable(start, end, height_map):
    x_start, y_start = start
    x_end, y_end = end
    # can climb up to current_height + 1 for a valid next step
    start_letter = height_map[y_start][x_start]
    start_height = ord('a') if ord(start_letter) == ord('S') else ord(start_letter)  # start indicator 'S' == height 'a'
    end_letter = height_map[y_end][x_end]
    end_height = ord('z') if ord(end_letter) == ord('E') else ord(end_letter)
    return end_height <= (start_height + 1)


def next_step_options(start, height_map, visited):
    x, y = start
    candidate_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    max_x = len(height_map[0])
    max_y = len(height_map)
    filtered_positions = [
        point
        for point in candidate_positions
        if 0 <= point[0] < max_x and 0 <= point[1] < max_y and point not in visited
           and is_reachable((x, y), point, height_map)
    ]
    return filtered_positions


def bfs(start_position, end_position, height_map):
    visited = set()
    distance_values = {start_position: 0}
    queue = [start_position]
    while queue:
        this = queue.pop(0)
        if this not in visited:
            visited.add(this)
            for next_pos in next_step_options(this, height_map, visited):
                distance_value = distance_values[this] + 1
                distance_values[next_pos] = distance_value
                if next_pos == end_position:
                    return distance_value
                queue.append(next_pos)


def find_route(input_filename):
    height_map = load_map(input_filename)
    start_position = find_target(height_map, target='S')
    end_position = find_target(height_map, target='E')
    return bfs(start_position, end_position, height_map)


def test__find_route():
    assert 31 == find_route('day12_test_input.txt')


def test__find_next_step_options():
    assert [(1, 0), (0, 1)] == next_step_options((0, 0), TEST_HEIGHT_MAP, set())
    assert [(0, 3)] == next_step_options((0, 2), TEST_HEIGHT_MAP, {(0, 1), })


def minimum_path(input_filename):
    height_map = load_map(input_filename)
    start_positions = [
        (column, row)
        for row, line in enumerate(height_map)
        for column, item in enumerate(line)
        if item == 'a'
    ]
    end_position = find_target(height_map, target='E')
    route_lengths = {
        start: bfs(start, end_position, height_map)
        for start in start_positions
    }
    return min(v for v in route_lengths.values() if v is not None)


def test__minimum_path():
    assert 29 == minimum_path('day12_test_input.txt')


def test__part1():
    assert 534 == find_route('day12_real_input.txt')


def test__part2():
    """ takes about 10 seconds ... """
    assert 525 == minimum_path('day12_real_input.txt')
