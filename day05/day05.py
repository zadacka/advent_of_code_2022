import re


class MoveInstruction:
    def __init__(self, input_string) -> None:
        super().__init__()
        match = re.search(r"move (\d*) from (\d*) to (\d*)", input_string)
        assert match, 'Could not translate {} into a move instruction'
        self.count, self.origin, self.destination = match.group(1, 2, 3)
        self.count = int(self.count)
        # fix the origin/destination to be zero indexed
        self.origin = int(self.origin) -1
        self.destination = int(self.destination) -1

    def __eq__(self, other):
        isinstance(other, MoveInstruction)
        return self.count == other.count and self.origin == other.origin and self.destination == other.destination


def parse_crane_input(input_file):
    stack_rows = []
    stack_count = 0
    move_instructions = []

    with open(input_file) as f:
        for line in f.readlines():
            if line.startswith(' 1 '):
                stack_count = len(line.split())
            elif line.startswith('move'):
                move_instructions.append(MoveInstruction(line))
            else:
                stack_rows.append(line)

    stack_state = [[] for _ in range(stack_count)]
    for stack_row in reversed(stack_rows):
        for column, value in enumerate(stack_row[1::4]):
            if value != ' ':
                stack_state[column].append(value)

    return stack_state, move_instructions


class LoadingCrane:
    def __init__(self, input_filename) -> None:
        super().__init__()
        self.stacks, self.instructions = parse_crane_input(input_filename)

    def do_moves(self, move_multiple_crates=False):
        for instruction in self.instructions:
            if move_multiple_crates:
                crates_to_move = self.stacks[instruction.origin][-instruction.count:]
                self.stacks[instruction.origin] = self.stacks[instruction.origin][:-instruction.count]
                self.stacks[instruction.destination].extend(crates_to_move)
            else:
                for _ in range(instruction.count):
                    crate_to_move = self.stacks[instruction.origin].pop()
                    self.stacks[instruction.destination].append(crate_to_move)

    def report_top_crates(self):
        return ''.join(crate[-1] for crate in self.stacks)


def test__move_instruction():
    instruction = MoveInstruction("move 1 from 2 to 1")
    assert instruction.count == 1
    assert instruction.origin == 1
    assert instruction.destination == 0

def test__part1_test():
    loading_crane = LoadingCrane('day05_test_input.txt')
    assert loading_crane.stacks == [
        ['Z', 'N'],
        ['M', 'C', 'D'],
        ['P']
    ]
    assert loading_crane.instructions == [
        MoveInstruction("move 1 from 2 to 1"),
        MoveInstruction("move 3 from 1 to 3"),
        MoveInstruction("move 2 from 2 to 1"),
        MoveInstruction("move 1 from 1 to 2"),
    ]
    loading_crane.do_moves()
    assert 'CMZ' == loading_crane.report_top_crates()

    loading_crane = LoadingCrane('day05_real_input.txt')
    loading_crane.do_moves()
    assert 'RLFNRTNFB' == loading_crane.report_top_crates()


def test__part2():
    loading_crane = LoadingCrane('day05_test_input.txt')
    loading_crane.do_moves(move_multiple_crates=True)
    assert 'MCD' == loading_crane.report_top_crates()

    loading_crane = LoadingCrane('day05_real_input.txt')
    loading_crane.do_moves(move_multiple_crates=True)
    assert 'RLFNRTNFB' == loading_crane.report_top_crates()