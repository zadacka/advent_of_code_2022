def count_calories(test_file, top_n=1):
    calorie_totals = [0]
    with open(test_file) as f:
        for line in f.readlines():
            if line != '\n':
                calorie_totals[-1] += int(line)
            else:
                calorie_totals.append(0)

    return sum(sorted(calorie_totals)[-top_n:])


def test__calorie_count():
    expected = 24000
    assert count_calories('day01_test_input.txt') == expected


def test__top_three_calorie_count():
    expected = 45000
    assert count_calories('day01_test_input.txt', 3) == expected


if __name__ == '__main__':
    print("Elf with most calories has: {}".format(count_calories('day01_real_input.txt')))
    print("Top 3 most calorie carrying elves have {}".format(count_calories('day01_real_input.txt', 3)))
