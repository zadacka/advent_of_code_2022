import itertools


def calculate_item_value(item):
    unicode_offset = 96 if item.islower() else 38
    return ord(item) - unicode_offset


def find_common_items(backpack):
    backpack = backpack.strip()  # get rid of terminal /n if it exists
    compartment_size = len(backpack) // 2
    first_compartment = backpack[:compartment_size]
    second_compartment = backpack[compartment_size:]
    common_items = set(first_compartment).intersection(set(second_compartment))
    return common_items


def grouper(size, iterable):
    it = iter(iterable)
    while True:
        group = tuple(itertools.islice(it, None, size))
        if not group:
            break
        yield group


def get_backpack_values(input_filename):
    backpack_values = []
    with open(input_filename) as f:
        for backpack in f.readlines():
            common_items = find_common_items(backpack)
            assert len(common_items) == 1, 'There should only be one item common to both compartments!'
            item = common_items.pop()
            item_value = calculate_item_value(item)
            backpack_values.append(item_value)
    return sum(backpack_values)


def test__calculate_value():
    assert {'p'} == find_common_items('vJrwpWtwJgWrhcsFMMfFFhFp')
    assert 16 == calculate_item_value('p')

    assert {'L'} == find_common_items('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL')
    assert 38 == calculate_item_value('L')

    assert {'P'} == find_common_items('PmmdzqPrVvPwwTWBwg')
    assert 42 == calculate_item_value('P')

    assert {'v'} == find_common_items('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn')
    assert 22 == calculate_item_value('v')

    assert {'t'} == find_common_items('ttgJtRGJQctTZtZT')
    assert 20 == calculate_item_value('t')

    assert {'s'} == find_common_items('CrZsJsPPZsGzwwsLwLmpwMDw')
    assert 19 == calculate_item_value('s')


def get_backpack_priority_items(input_filename):
    backpack_priority_items = []
    with open(input_filename) as f:
        for group in grouper(3, f.readlines()):
            backpack1, backpack2, backpack3 = group
            common_item = set(backpack1.strip()).intersection(set(backpack2.strip())).intersection(
                set(backpack3.strip()))
            assert len(common_item) == 1
            backpack_priority_items.append(common_item.pop())
    priority_item_values = [calculate_item_value(item) for item in backpack_priority_items]
    return sum(priority_item_values)


def test__get_backpack_value():
    assert get_backpack_values('day03_test_input.txt') == 157
    assert get_backpack_values('day03_real_input.txt') == 8515


def test__get_backpack_priority_item_value():
    assert get_backpack_priority_items('day03_test_input.txt') == 70
    assert get_backpack_priority_items('day03_real_input.txt') == 2434


if __name__ == '__main__':
    print('Backpack values from part 1: {}'.format(get_backpack_values('day03_real_input.txt')))
