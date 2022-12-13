from json import loads


def load_pairs_input(input_filename):
    with open(input_filename) as f:
        lines = f.readlines()
    stripped_lines = [loads(line) for line in lines if line != '\n']
    pairs = [(left, right) for left, right in zip(stripped_lines[0::2], stripped_lines[1::2])]
    return pairs


def test__load_pairs_input():
    actual = load_pairs_input('day13_test_input.txt')
    expected = [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
    ]
    assert actual == expected


def check_correct_order(left, right, check_list_length=True):
    """
    """
    if isinstance(left, int) and isinstance(right, int):
        # Rule 1: If both values are integers, the lower integer should come first.
        if left > right:
            return False
    elif isinstance(left, list) and isinstance(right, list):
        # Rule 2: If both values are lists keep checking... false if the right list runs out of items first
        # and no comparison makes a decision about the order, continue checking the next part of the input.
        if check_list_length and len(right) < len(left):
            return False
        for l2, r2 in zip(left, right):
            if check_correct_order(l2, r2) is False:
                return False
    elif isinstance(left, list) and isinstance(right, int):
        # Rule 3: If exactly one value is an integer, convert it to a list which contains that integer as its only value
        if check_correct_order(left, [right], check_list_length=False) is False:
            return False
    elif isinstance(left, int) and isinstance(right, list):
        # Rule 3: again
        if check_correct_order([left], right, check_list_length=False) is False:
            return False
    else:
        raise RuntimeError("Some crazy input brought me here: l='{}', r='{}'".format(left, right))

    return True


def test__check_right_order():
    assert check_correct_order([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])
    assert check_correct_order([[1], [2, 3, 4]], [[1], 4])
    assert not check_correct_order([9], [[8, 7, 6]])
    assert check_correct_order([[4, 4], 4, 4], [[4, 4], 4, 4, 4])
    assert not check_correct_order([7, 7, 7, 7], [7, 7, 7])
    assert check_correct_order([], [3])
    assert not check_correct_order([[[]]], [[]])
    assert not check_correct_order([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])


def count_correct_index_values(input_file):
    pairs = load_pairs_input(input_file)
    results = [check_correct_order(*pair) for pair in pairs]
    result = 0
    for index, check in enumerate(results, start=1):
        if check:
            result += index
    return result


def test__part1():
    assert 13 == count_correct_index_values('day13_test_input.txt')
    assert 627 == count_correct_index_values('day13_real_input.txt')
