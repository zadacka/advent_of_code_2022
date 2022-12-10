
def perform_move(head, tail, move):
    assert move in ('L', 'R', 'U', 'D')
    hx, hy = head
    tx, ty = tail

    if move == 'L':
        hx -= 1
    elif move == 'R':
        hx += 1
    elif move == 'U':
        hy += 1
    else:  # move == 'D':
        hy -= 1

    if abs(hx - tx) + abs(hy - ty) == 3:
        tx = tx + 1 if hx > tx else tx - 1
        ty = ty + 1 if hy > ty else ty - 1
        # tail must move diagonally towards head
    elif abs(hx - tx) == 2:
        tx = tx + 1 if hx > tx else tx - 1
        # tail must move horizontally towards head
    elif abs(hy - ty) == 2:
        ty = ty + 1 if hy > ty else ty - 1
        # tail must move vertically towards head
    else:
        pass  # nothing needs to move

    return [hx, hy], [tx, ty]


def calculate_tail_positions(input_file):
    tail_positions = {(0, 0), }

    head_position = [0, 0]
    tail_position = [0, 0]

    with open(input_file) as f:
        moves = f.readlines()

    for move in moves:
        move_direction, move_count = move.strip().split()
        for _ in range(int(move_count)):
            head_position, tail_position = perform_move(head_position, tail_position, move_direction)
            tail_positions.add((tail_position[0], tail_position[1]))
    return tail_positions


def test__perform_move():
    head, tail = perform_move([0, 0], [0, 0], 'R')
    assert head == [1, 0]
    assert tail == [0, 0]

    head, tail = perform_move([1, 0], [0, 0], 'R')
    assert head == [2, 0]
    assert tail == [1, 0]

    head, tail = perform_move([1, 1], [0, 0], 'R')
    assert head == [2, 1]
    assert tail == [1, 1]

    head, tail = perform_move([1, 0], [0, 0], 'U')
    assert head == [1, 1]
    assert tail == [0, 0]


def test__part1():
    assert 13 == len(calculate_tail_positions('day09_test_input.txt'))
    assert 6090 == len(calculate_tail_positions('day09_real_input.txt'))
