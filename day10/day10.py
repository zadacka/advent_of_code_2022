def calculate_x_values(input_file):
    with open(input_file) as f:
        lines = f.readlines()
    return _calculate_x_values(lines)


def _calculate_x_values(lines):
    x_values = [0, 1, ]  # pad first (zero) entry so we can look up by 'during' cycle for the result (index 1)
    for line in lines:
        # every instruction takes at least one cycle when the x_value stays the same
        x_values.append(x_values[-1])
        if line.startswith('noop'):
            # nothing further to do
            pass
        else:
            # additional cycle elapses and then the addition is processed
            instruction, argument = line.strip().split()
            assert instruction == 'addx'
            x_values.append(x_values[-1] + int(argument))
    return x_values


def test___calculate_x_values():
    x_values = _calculate_x_values(["noop\n", "addx 3\n", "addx -5"])
    assert x_values == [0, 1, 1, 1, 4, 4, -1]


def calculate_signal_strength(x_values, sample=(20, 60, 100, 140, 180, 220)):
    return sum(x_values[sample_point] * sample_point for sample_point in sample)


def test__calculate_x_values():
    x_values = calculate_x_values('day10_test_input.txt')
    assert 19 == x_values[60]
    assert 18 == x_values[100]
    assert 21 == x_values[140]
    assert 16 == x_values[180]
    assert 18 == x_values[220]
    assert 13140 == calculate_signal_strength(x_values)


def test__part1():
    x_values = calculate_x_values('day10_real_input.txt')
    assert 14560 == calculate_signal_strength(x_values)


def render(x_values):
    result = ""
    for row in range(0, 6):
        for col in range(0, 40):
            index = (row * 40) + col + 1  # display indexing is 0, x_values indexing is 1
            sprite_position = x_values[index]
            sprite_pixels = {sprite_position - 1, sprite_position, sprite_position + 1}
            if col in sprite_pixels:
                result += '#'
            else:
                result += '.'
        result += '\n'
    return result


def test__render():
    expected = """\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
    x_values = calculate_x_values('day10_test_input.txt')
    assert expected == render(x_values)


def test__part2():
    expected = """\
####.#..#.###..#..#.####.###..#..#.####.
#....#.#..#..#.#..#.#....#..#.#..#....#.
###..##...#..#.####.###..#..#.#..#...#..
#....#.#..###..#..#.#....###..#..#..#...
#....#.#..#.#..#..#.#....#....#..#.#....
####.#..#.#..#.#..#.####.#.....##..####.
"""
    x_values = calculate_x_values('day10_real_input.txt')
    assert expected == render(x_values)
