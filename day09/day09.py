def move_head(head, move):
    assert move in ('L', 'R', 'U', 'D')
    hx, hy = head

    if move == 'L':
        hx -= 1
    elif move == 'R':
        hx += 1
    elif move == 'U':
        hy += 1
    else:  # move == 'D':
        hy -= 1

    return [hx, hy]


def update_tail(head, tail):
    hx, hy = head
    tx, ty = tail
    if abs(hx - tx) + abs(hy - ty) >= 3:  # ouch - had to look for help here, I had == 2 and it didn't work
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
    return [tx, ty]


def print_tail_positions(tail_positions):
    result = ''
    xmin = min(x for x, y in tail_positions)
    xmax = max(x for x, y in tail_positions)
    ymin = min(y for x, y in tail_positions)
    ymax = max(y for x, y in tail_positions)
    for y in range(ymin -1, ymax + 1):
        for x in range(xmin -1 , xmax + 1):
            if (x, y) in tail_positions:
               result += '#'
            else:
                result += '.'
        result += '\n'
    print(result)


def calculate_tail_positions(input_file, length=2):
    tail_positions = {(0, 0), }

    chain = [[0, 0] for _ in range(length)]

    with open(input_file) as f:
        moves = f.readlines()

    for move in moves:
        move_direction, move_count = move.strip().split()
        for _ in range(int(move_count)):
            chain[0] = move_head(chain[0], move_direction)
            for index in range(1, length):
                chain[index] = update_tail(chain[index - 1], chain[index])
            tail_positions.add(tuple(chain[-1]))
    return tail_positions


def test__perform_move():
    head = move_head([0, 0], 'R')
    assert head == [1, 0]
    tail = update_tail(head, [0, 0])
    assert tail == [0, 0]

    head = move_head([1, 0], 'R')
    assert head == [2, 0]
    tail = update_tail(head, [0, 0])
    assert tail == [1, 0]

    head = move_head([1, 1], 'R')
    assert head == [2, 1]
    tail = update_tail(head, [0, 0])
    assert tail == [1, 1]

    head = move_head([1, 0], 'U')
    assert head == [1, 1]
    tail = update_tail(head, [0, 0])
    assert tail == [0, 0]


def test__part1():
    assert 13 == len(calculate_tail_positions('day09_test_input.txt'))
    assert 6090 == len(calculate_tail_positions('day09_real_input.txt'))


def test__part2():
    assert 1 == len(calculate_tail_positions('day09_test_input.txt', length=10))
    assert 36 == len(calculate_tail_positions('day09_test_input2.txt', length=10))
    assert 2566 == len(calculate_tail_positions('day09_real_input.txt', length=10))
