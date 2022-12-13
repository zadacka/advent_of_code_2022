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


def check_correct_order(left, right):
    """
    -1 is False, 1 is True, 0 is 'no comparison' (used by recursive calls)
    """
    if isinstance(left, int) and isinstance(right, int):
        # Rule 1: If both values are integers, the lower integer should come first.
        return 1 if left < right else -1 if left > right else 0
    elif isinstance(left, list) and isinstance(right, list):
        # Rule 2: If both values are lists keep checking... false if the right list runs out of items first
        # and no comparison makes a decision about the order, continue checking the next part of the input.
        for comparison_result in (check_correct_order(l, r) for l, r in zip(left, right)):
            if comparison_result != 0:
                return comparison_result
        # THIS MESSED ME UP ... only use the list length check if element check has not been decisive
        return -1 if len(right) < len(left) else 1 if len(left) < len(right) else 0
    elif isinstance(left, list) and isinstance(right, int):
        # Rule 3: If exactly one value is an integer, convert it to a list which contains that integer as its only value
        return check_correct_order(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        # Rule 3: again
        return check_correct_order([left], right)
    else:
        raise RuntimeError("Some crazy input brought me here: l='{}', r='{}'".format(left, right))


def test__check_right_order():
    assert 1 == check_correct_order([1, 1, 3, 1, 1], [1, 1, 5, 1, 1])
    assert 1 == check_correct_order([[1], [2, 3, 4]], [[1], 4])
    assert -1 == check_correct_order([9], [[8, 7, 6]])
    assert 1 == check_correct_order([[4, 4], 4, 4], [[4, 4], 4, 4, 4])
    assert -1 == check_correct_order([7, 7, 7, 7], [7, 7, 7])
    assert 1 == check_correct_order([], [3])
    assert -1 == check_correct_order([[[]]], [[]])
    assert -1 == check_correct_order([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])


def count_correct_index_values(input_file):
    pairs = load_pairs_input(input_file)
    results = [check_correct_order(*pair) for pair in pairs]
    result = sum(index for index, check in enumerate(results, start=1) if check == 1)
    return result

def test__part1():
    assert 13 == count_correct_index_values('day13_test_input.txt')
    assert 5366 == count_correct_index_values('day13_real_input.txt')
