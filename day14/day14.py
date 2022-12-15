def load_rocks(input_file):
    def format_point(point):
        return tuple(int(x_y) for x_y in point.split(','))

    with open(input_file) as f:
        return [[format_point(point) for point in line.split('->')] for line in f.readlines()]


def points_in_between(start, end):
    start_x, start_y = start
    end_x, end_y = end
    if start_x == end_x:
        return {(start_x, y) for y in range(min(start_y, end_y), max(start_y, end_y) + 1)}
    elif start_y == end_y:
        return {(x, start_y) for x in range(min(start_x, end_x), max(start_x, end_x) + 1)}
    else:
        raise RuntimeError()


def expand_rocks(rocks):
    result = set()
    for formation in rocks:
        for start, end in zip(formation, formation[1:]):
            for rock in points_in_between(start, end):
                result.add(rock)
    return result


TEST_ROCKS = [
    [(498, 4), (498, 6), (496, 6)],
    [(503, 4), (502, 4), (502, 9), (494, 9)]
]


def test__expand_rocks():
    assert {(494, 9), (495, 9), (496, 6), (496, 9), (497, 6), (497, 9), (498, 4), (498, 5), (498, 6),
            (498, 9), (499, 9), (500, 9), (501, 9), (502, 4), (502, 5), (502, 6), (502, 7), (502, 8), (502, 9),
            (503, 4)} == expand_rocks(TEST_ROCKS)


def test__load_rocks():
    assert load_rocks('day14_test_input.txt') == TEST_ROCKS


class Reservoir:

    def __init__(self, rock_formations) -> None:
        super().__init__()
        self.max_x = max(max(point[0] for point in rock) for rock in rock_formations)
        self.max_y = max(max(point[1] for point in rock) for rock in rock_formations)
        self.min_x = min(min(point[0] for point in rock) for rock in rock_formations)
        self.min_y = min(min(point[1] for point in rock) for rock in rock_formations)

        self.falling_sand = None

        self.rocks = expand_rocks(rock_formations)
        self.sand = set()

    def draw_reservoir(self):
        result = ''
        x_range = self.max_x - self.min_x
        for y in range(0, self.max_y + 1):
            for x in range(self.min_x, self.min_x + x_range + 1):
                if (x, y) in self.rocks:
                    result += '#'
                elif (x, y) in self.sand:
                    result += 'o'
                else:
                    result += '.'
            result += '\n'
        return result

    def add_sand(self, floor_exists=False):
        x, y = (500, 0)
        blocked_spaces = self.rocks.union(self.sand)
        while True:
            if x < self.min_x or x > self.max_x or y > self.max_y:
                return False

            if (x, y + 1) not in blocked_spaces:
                y += 1
            elif (x - 1, y + 1) not in blocked_spaces:
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in blocked_spaces:
                x += 1
                y += 1
            else:
                self.sand.add((x, y))
                return True

def test__draw_map():
    reservoir = Reservoir(TEST_ROCKS)
    assert reservoir.draw_reservoir() == """\
..........
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
........#.
#########.
"""

def test__adding_sand():
    test_formations = load_rocks('day14_test_input.txt')
    reservoir = Reservoir(test_formations)
    sand_added = 0
    while(reservoir.add_sand()):
        sand_added += 1
    assert 24 == sand_added

def test__adding_sand():
    test_formations = load_rocks('day14_real_input.txt')
    reservoir = Reservoir(test_formations)
    sand_added = 0
    while(reservoir.add_sand()):
        sand_added += 1
    assert 24 == sand_added