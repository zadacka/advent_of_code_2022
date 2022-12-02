def part_one_score_function(my_move, their_move):
    their_move = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}[their_move]
    my_move = {'X': 'rock', 'Y': 'paper', 'Z': 'scissors'}[my_move]

    outcomes = {
        ('rock', 'rock'): 'draw',
        ('rock', 'paper'): 'lose',
        ('rock', 'scissors'): 'win',

        ('paper', 'rock'): 'win',
        ('paper', 'paper'): 'draw',
        ('paper', 'scissors'): 'lose',

        ('scissors', 'rock'): 'lose',
        ('scissors', 'paper'): 'win',
        ('scissors', 'scissors'): 'draw',
    }
    outcome_scores = {'lose': 0, 'draw': 3, 'win': 6}
    choice_scores = {'rock': 1, 'paper': 2, 'scissors': 3}

    game_outcome = outcomes[(my_move, their_move)]

    return outcome_scores[game_outcome] + choice_scores[my_move]


def part_two_score_function(target_outcome, their_move):
    their_move = {'A': 'rock', 'B': 'paper', 'C': 'scissors'}[their_move]
    target_outcome = {'X': 'lose', 'Y': 'draw', 'Z': 'win'}[target_outcome]
    move_required = {
        ('rock', 'lose'): 'scissors',
        ('rock', 'draw'): 'rock',
        ('rock', 'win'): 'paper',
        ('paper', 'lose'): 'rock',
        ('paper', 'draw'): 'paper',
        ('paper', 'win'): 'scissors',
        ('scissors', 'lose'): 'paper',
        ('scissors', 'draw'): 'scissors',
        ('scissors', 'win'): 'rock',
    }
    my_move = move_required[(their_move, target_outcome)]

    result_scores = {'lose': 0, 'draw': 3, 'win': 6}
    choice_scores = {'rock': 1, 'paper': 2, 'scissors': 3}

    return result_scores[target_outcome] + choice_scores[my_move]


def calculate_score(input_filename, score_function):
    final_score = 0
    with open(input_filename) as f:
        for line in f.readlines():
            their_move, my_move = line.split()
            final_score += score_function(my_move, their_move)
    return final_score


def test__calculate_score_part_1():
    expected = 15
    assert calculate_score('day02_test_input.txt', part_one_score_function) == expected


def test__calculate_score_part_2():
    expected = 12
    assert calculate_score('day02_test_input.txt', part_two_score_function) == expected


if __name__ == '__main__':
    print("Predicted score: {}".format(calculate_score('day02_real_input.txt', part_one_score_function)))
    print("Predicted score part 2: {}".format(calculate_score('day02_real_input.txt', part_two_score_function)))
