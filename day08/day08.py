def trees_by_row(input_file):
    with open(input_file) as f:
        content = f.readlines()
    return [[tree for tree in row.strip()] for row in content]


def test__trees_by_row():
    trees = trees_by_row('day08_test_input.txt')
    assert trees == [
        ['3', '0', '3', '7', '3'],
        ['2', '5', '5', '1', '2'],
        ['6', '5', '3', '3', '2'],
        ['3', '3', '5', '4', '9'],
        ['3', '5', '3', '9', '0']
    ]


def visible_trees_in_list(input_list):
    visible_trees = [
        index for index, tree_height in enumerate(input_list)
        if (
                index == 0 or  # first tree always visible
                index == len(input_list) - 1 or  # last tree always visible
                max(input_list[:index]) < tree_height or  # visible from the left
                max(input_list[index + 1:]) < tree_height)  # visible from the right
    ]
    return visible_trees


def scenic_score(index, input_list, look_right=False):
    """ not exactly intuitive 'scoring' system ... need to read AoC #8 to get the story """
    if look_right:  # if calculating view score to the right we just flip things, fix the index
        input_list = list(reversed(input_list))
        index = len(input_list) - index - 1

    if index == 0:  # view score at the edge is always zero
        return 0

    score = 0
    for tree in reversed(input_list[:index]):  # looking left from our position, how far can we see?
        score += 1
        if tree >= input_list[index]:  # stop if a tree is equal or taller than us
            break
    return score


def test__scenic_score():
    assert 0 == scenic_score(0, ['3', '0', '3', '7', '3'])
    assert 1 == scenic_score(1, ['3', '0', '3', '7', '3'])
    assert 3 == scenic_score(3, ['3', '0', '3', '7', '3'])
    assert 2 == scenic_score(0, ['3', '0', '3', '7', '3'], look_right=True)


def scenic_score_list(input_list):
    scenic_scores = [
        scenic_score(index, input_list) * scenic_score(index, input_list, look_right=True)
        for index, _ in enumerate(input_list)
    ]
    return scenic_scores


def test__scenic_scores_list():
    assert [(0 * 1), (1 * 1), (1 * 2), (1 * 1), (2 * 0)] == scenic_score_list(['2', '5', '5', '1', '2'])


def get_visible_trees(input_file):
    trees = trees_by_row(input_file)
    visible_trees = set()

    for row_index, row in enumerate(trees):
        for column_index in visible_trees_in_list(row):
            visible_trees.add((row_index, column_index))

    # flip the array, go through it again
    for col_index, col in enumerate(zip(*trees)):
        for row_index in visible_trees_in_list(col):
            visible_trees.add((row_index, col_index))
    return visible_trees


def test__visible_trees_in_list():
    assert [0, 3, 4] == visible_trees_in_list(['3', '0', '3', '7', '3'])


def get_scenic_scores_trees(input_file):
    trees = trees_by_row(input_file)
    scenic_scores = {}

    for row_index, row in enumerate(trees):
        for column_index, score in enumerate(scenic_score_list(row)):
            scenic_scores[(row_index, column_index)] = score

    # flip the array, go through it again
    for col_index, col in enumerate(zip(*trees)):
        for row_index, score in enumerate(scenic_score_list(col)):
            scenic_scores[(row_index, col_index)] *= score
    return scenic_scores


def test__part1():
    assert 21 == len(get_visible_trees('day08_test_input.txt'))
    assert 1688 == len(get_visible_trees('day08_real_input.txt'))


def test__part2():
    assert 8 == max(get_scenic_scores_trees('day08_test_input.txt').values())
    assert 410400 == max(get_scenic_scores_trees('day08_real_input.txt').values())
