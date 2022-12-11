import io
import math
import unittest.mock


class Monkey:

    def __init__(self, starting_items, op, op_arg, test_divisor, target_if_true, target_if_false) -> None:
        super().__init__()
        self.starting_items = starting_items
        self.op = op
        self.op_arg = op_arg
        self.test_divisor = test_divisor
        self.target_if_true = target_if_true
        self.target_if_false = target_if_false
        self.times_inspect_called = 0
        self.worry_limit = None

    def __eq__(self, other):
        return all([
            isinstance(other, Monkey),
            self.starting_items == other.starting_items,
            self.op == other.op,
            self.op_arg == other.op_arg,
            self.test_divisor == other.test_divisor,
            self.target_if_true == other.target_if_true,
            self.target_if_false == other.target_if_false,
        ])

    def inspect(self):
        self.times_inspect_called += 1
        item = self.starting_items.pop(0)
        print('  Monkey inspects an item with a worry level of {}.'.format(item))
        operand = item if self.op_arg == 'old' else int(self.op_arg)
        if self.op == '+':
            new_item_value = item + operand
            print('    Worry level increases by {} to {}.'.format(operand, new_item_value))
        elif self.op == '*':
            new_item_value = item * operand
            print('    Worry level is multiplied by {} to {}.'.format(
                'itself' if operand == item else operand, new_item_value))
        else:
            raise RuntimeError("Don't know how to handle op: {}".format(self.op))

        if self.worry_limit:
            _, modulus = divmod(new_item_value, self.worry_limit)
            bored_value = modulus
            print("    Monkey gets bored with item. Worry level limited mod worry limit {}.".format(self.worry_limit))
        else:
            bored_value = math.floor(new_item_value / 3)
            print("    Monkey gets bored with item. Worry level is divided by 3 to {}.".format(bored_value))

        quotient, mod = divmod(bored_value, self.test_divisor)
        if mod == 0:
            print("    Current worry level is divisible by {}.".format(self.test_divisor))
            print("    Item with worry level {} is thrown to monkey {}.".format(bored_value, self.target_if_true))
            target = self.target_if_true
        else:
            print("    Current worry level is not divisible by {}.".format(self.test_divisor))
            print("    Item with worry level {} is thrown to monkey {}.".format(bored_value, self.target_if_false))
            target = self.target_if_false
        return bored_value, target

    def set_worry_limit(self, worry_limit):
        self.worry_limit = worry_limit


def test__monkey_equality():
    m1 = Monkey(starting_items=[79, 98], op='*', op_arg='19', test_divisor=23, target_if_true=2,
                target_if_false=3)
    m2 = Monkey(starting_items=[10], op='*', op_arg='19', test_divisor=23, target_if_true=2, target_if_false=3)
    assert m1 == m1
    assert m1 != m2


def parse_monkeys(input_file):
    result = []
    with open(input_file) as f:
        lines = f.readlines()

    monkey_number = 0
    monkey_items = []
    monkey_operation = ''
    monkey_operation_arg = ''
    monkey_test_divisor = 0
    monkey_target_if_true = 0
    monkey_target_if_false = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue  # empty line between monkeys
        if line.startswith('Monkey'):
            _ = int(line.split()[-1].split(':')[0])
        elif line.startswith('Starting items'):
            monkey_items = [int(item.strip()) for item in line.split(':')[1].split(',')]
        elif line.startswith('Operation:'):
            left, op, right = line.split('=')[1].strip().split()
            assert left == 'old'  # assert that it follows the pattern 'new = old <op> <op_arg>'
            monkey_operation = op
            monkey_operation_arg = right
        elif line.startswith('Test:'):
            monkey_test_divisor = int(line.split()[-1])
        elif line.startswith('If true'):
            monkey_target_if_true = int(line.split()[-1])
        elif line.startswith('If false'):
            monkey_target_if_false = int(line.split()[-1])
            result.append(
                Monkey(
                    starting_items=monkey_items, op=monkey_operation, op_arg=monkey_operation_arg,
                    test_divisor=monkey_test_divisor, target_if_true=monkey_target_if_true,
                    target_if_false=monkey_target_if_false
                )
            )
        else:
            raise RuntimeError('Unsure how to handle: {}'.format(line))
    return result


def test__parse_monkeys():
    actual = parse_monkeys('day11_test_input.txt')
    expected = [
        Monkey(starting_items=[79, 98], op='*', op_arg='19', test_divisor=23, target_if_true=2, target_if_false=3),
        Monkey(starting_items=[54, 65, 75, 74], op='+', op_arg='6', test_divisor=19, target_if_true=2,
               target_if_false=0),
        Monkey(starting_items=[79, 60, 97], op='*', op_arg='old', test_divisor=13, target_if_true=1, target_if_false=3),
        Monkey(starting_items=[74], op='+', op_arg='3', test_divisor=17, target_if_true=0, target_if_false=1),
    ]
    for e, a in zip(actual, expected):
        assert e == a


def process_items(monkeys, rounds=1):
    for round in range(rounds):
        for monkey_number, monkey in enumerate(monkeys):
            print("Monkey {}:".format(monkey_number))
            while monkey.starting_items:
                value, target = monkey.inspect()
                monkeys[target].starting_items.append(value)
    return monkeys


@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
def test__process_one_round(mock_stdout):
    monkeys = parse_monkeys('day11_test_input.txt')
    state = process_items(monkeys)
    expected_story = """\
Monkey 0:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by 19 to 1501.
    Monkey gets bored with item. Worry level is divided by 3 to 500.
    Current worry level is not divisible by 23.
    Item with worry level 500 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 98.
    Worry level is multiplied by 19 to 1862.
    Monkey gets bored with item. Worry level is divided by 3 to 620.
    Current worry level is not divisible by 23.
    Item with worry level 620 is thrown to monkey 3.
Monkey 1:
  Monkey inspects an item with a worry level of 54.
    Worry level increases by 6 to 60.
    Monkey gets bored with item. Worry level is divided by 3 to 20.
    Current worry level is not divisible by 19.
    Item with worry level 20 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 65.
    Worry level increases by 6 to 71.
    Monkey gets bored with item. Worry level is divided by 3 to 23.
    Current worry level is not divisible by 19.
    Item with worry level 23 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 75.
    Worry level increases by 6 to 81.
    Monkey gets bored with item. Worry level is divided by 3 to 27.
    Current worry level is not divisible by 19.
    Item with worry level 27 is thrown to monkey 0.
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 6 to 80.
    Monkey gets bored with item. Worry level is divided by 3 to 26.
    Current worry level is not divisible by 19.
    Item with worry level 26 is thrown to monkey 0.
Monkey 2:
  Monkey inspects an item with a worry level of 79.
    Worry level is multiplied by itself to 6241.
    Monkey gets bored with item. Worry level is divided by 3 to 2080.
    Current worry level is divisible by 13.
    Item with worry level 2080 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 60.
    Worry level is multiplied by itself to 3600.
    Monkey gets bored with item. Worry level is divided by 3 to 1200.
    Current worry level is not divisible by 13.
    Item with worry level 1200 is thrown to monkey 3.
  Monkey inspects an item with a worry level of 97.
    Worry level is multiplied by itself to 9409.
    Monkey gets bored with item. Worry level is divided by 3 to 3136.
    Current worry level is not divisible by 13.
    Item with worry level 3136 is thrown to monkey 3.
Monkey 3:
  Monkey inspects an item with a worry level of 74.
    Worry level increases by 3 to 77.
    Monkey gets bored with item. Worry level is divided by 3 to 25.
    Current worry level is not divisible by 17.
    Item with worry level 25 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 500.
    Worry level increases by 3 to 503.
    Monkey gets bored with item. Worry level is divided by 3 to 167.
    Current worry level is not divisible by 17.
    Item with worry level 167 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 620.
    Worry level increases by 3 to 623.
    Monkey gets bored with item. Worry level is divided by 3 to 207.
    Current worry level is not divisible by 17.
    Item with worry level 207 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 1200.
    Worry level increases by 3 to 1203.
    Monkey gets bored with item. Worry level is divided by 3 to 401.
    Current worry level is not divisible by 17.
    Item with worry level 401 is thrown to monkey 1.
  Monkey inspects an item with a worry level of 3136.
    Worry level increases by 3 to 3139.
    Monkey gets bored with item. Worry level is divided by 3 to 1046.
    Current worry level is not divisible by 17.
    Item with worry level 1046 is thrown to monkey 1.
"""
    assert expected_story == mock_stdout.getvalue()


@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
def test__process_twenty_rounds(mock_stdout):
    monkeys = parse_monkeys('day11_test_input.txt')
    state = process_items(monkeys, rounds=20)
    monkey_activity = [monkey.times_inspect_called for monkey in state]
    assert [101, 95, 7, 105] == monkey_activity
    sorted_monkey_activity = list(sorted(monkey_activity))
    monkey_business = sorted_monkey_activity[-1] * sorted_monkey_activity[-2]
    assert 10605 == monkey_business


@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
def test__part1(mock_stdout):
    monkeys = parse_monkeys('day11_real_input.txt')
    state = process_items(monkeys, rounds=20)
    assert 76728 == calculate_monkey_business_score(state)


def calculate_monkey_business_score(state):
    monkey_activity = [monkey.times_inspect_called for monkey in state]
    sorted_monkey_activity = list(sorted(monkey_activity))
    monkey_business = sorted_monkey_activity[-1] * sorted_monkey_activity[-2]
    return monkey_business


@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
def test__using_a_worry_limit(mock_stdout):
    monkeys = parse_monkeys('day11_test_input.txt')
    worry_limit = math.prod([monkey.test_divisor for monkey in monkeys])
    for monkey in monkeys:
        monkey.set_worry_limit(worry_limit)

    state = process_items(monkeys, rounds=1)
    assert [2, 4, 3, 6] == [monkey.times_inspect_called for monkey in monkeys]

    state = process_items(state, rounds=19)
    assert [99, 97, 8, 103] == [monkey.times_inspect_called for monkey in monkeys]

    state = process_items(state, rounds=980)
    assert [5204, 4792, 199, 5192] == [monkey.times_inspect_called for monkey in monkeys]

    state = process_items(state, rounds=1000)
    assert [10419, 9577, 392, 10391] == [monkey.times_inspect_called for monkey in monkeys]

    state = process_items(state, rounds=8000)
    assert [52166, 47830, 1938, 52013] == [monkey.times_inspect_called for monkey in monkeys]


@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
def test__part2(mock_stdout):
    monkeys = parse_monkeys('day11_real_input.txt')
    worry_limit = math.prod([monkey.test_divisor for monkey in monkeys])
    for monkey in monkeys:
        monkey.set_worry_limit(worry_limit)

    state = process_items(monkeys, rounds=10000)
    assert 21553910156 == calculate_monkey_business_score(state)
