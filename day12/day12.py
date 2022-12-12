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
                return row, column
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


def _find_route(route, height_map, target, viable_routes):
    if route[-1] == target:
        viable_routes.append(route)  # we have reached the end!
        return None

    def nearest_end(point):
        px, py = point
        tx, ty = target
        return (ty - py) ** 2 + (tx - px) ** 2

    next_steps = next_step_options(route, height_map)
    next_steps = sorted(next_steps, key=nearest_end)

    for next_step in next_steps:
        attempt = [point for point in route] + [next_step]
        _find_route(attempt, height_map, target, viable_routes)


def find_route(input_filename):
    height_map = load_map(input_filename)
    start_position = find_target(height_map, target='S')
    end_position = find_target(height_map, target='E')
    viable_routes = []
    _find_route([start_position, ], height_map, target=end_position, viable_routes=viable_routes)
    return min(viable_routes, key=len)


def test__find_route():
    assert 31 == len(find_route('day12_test_input.txt')) - 1


def test__find_next_step_options():
    assert [(1, 0), (0, 1)] == next_step_options([(0, 0)], TEST_HEIGHT_MAP)
    assert [(0, 3)] == next_step_options([(0, 0), (0, 1), (0, 2)], TEST_HEIGHT_MAP)


def test__part1():
    assert 0 == len(find_route('day12_real_input.txt')) - 1
