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


def find_start(heightmap):
    for row, line in enumerate(heightmap):
        for column, item in enumerate(line):
            if item == 'S':
                return (row, column)
    raise RuntimeError('Start Cell not found.')


def test__load_map():
    assert TEST_HEIGHT_MAP == load_map('day12_test_input.txt')


def test__find_start():
    assert (0, 0) == find_start(TEST_HEIGHT_MAP)


def is_reachable(start, end, height_map):
    x_start, y_start = start
    x_end, y_end = end
    # can climb up to current_height + 1 for a valid next step
    start_letter = height_map[y_start][x_start]
    start_height = ord('a') if ord(start_letter) == ord('S') else ord(start_letter)  # start indicator 'S' == height 'a'
    end_letter = height_map[y_end][x_end]
    end_height = ord('z') if ord(end_letter) == ord('E') else ord(end_letter)
    return end_height <= (start_height + 1)


def next_step_options(route_so_far, height_map):
    x, y = route_so_far[-1]
    candidate_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    max_x = len(height_map[0])
    max_y = len(height_map)
    filtered_positions = [
        point
        for point in candidate_positions
        if 0 <= point[0] < max_x and 0 <= point[1] < max_y and point not in route_so_far
           and is_reachable((x, y), point, height_map)
    ]
    return filtered_positions


def _find_route(route_so_far, height_map):
    end_x, end_y = route_so_far[-1]
    if height_map[end_y][end_x] == 'E':
        return route_so_far  # we have reached the end!

    candidate_next_steps = next_step_options(route_so_far, height_map)
    if not candidate_next_steps:
        return None

    viable_routes = []
    for next_step in candidate_next_steps:
        updated_route = [point for point in route_so_far] + [next_step]
        another_route = _find_route(updated_route, height_map)
        if another_route is not None:
            viable_routes.append(another_route)
    if viable_routes:
        return min(viable_routes, key=len)
    return None  # no route found


def find_route(input_filename):
    height_map = load_map(input_filename)
    start_position = find_start(height_map)
    return _find_route([start_position, ], height_map)


def test__find_route():
    assert 31 == len(find_route('day12_test_input.txt')) - 1


def test__find_next_step_options():
    assert [(1, 0), (0, 1)] == next_step_options([(0, 0)], TEST_HEIGHT_MAP)
    assert [(0, 3)] == next_step_options([(0, 0), (0, 1), (0, 2)], TEST_HEIGHT_MAP)

def test__part1():
    assert 0 == len(find_route('day12_real_input.txt')) - 1