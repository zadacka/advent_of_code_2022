def count_calories_1(test_file, top_n=1):
    with open(test_file) as f:
        calories = [
            sum([int(snack) for snack in elf.split('\n')])
            for elf in f.read().split('\n\n')
        ]
        return sum(sorted(calories)[-top_n:])


def count_calories2(test_file, top_n=1):
    with open(test_file) as f:
        elf_supplies = []
        snacks_so_far = 0
        for snack in f.readlines():
            if snack == '\n':
                elf_supplies.append(snacks_so_far)
                snacks_so_far = 0
            else:
                snacks_so_far += int(snack)
        elf_supplies.append(snacks_so_far)

        return sum(sorted(elf_supplies)[-top_n:])


def count_calories(test_file, top_n=1):
    with open(test_file) as f:
        elf_supplies = [0]
        for snack in f.readlines():
            if snack == '\n':
                elf_supplies.append(0)
            else:
                elf_supplies[-1] += int(snack)

        return sum(sorted(elf_supplies)[-top_n:])


def test__calorie_count():
    expected = 24000
    assert count_calories('day01_test_input.txt') == expected


def test__top_three_calorie_count():
    expected = 45000
    assert count_calories('day01_test_input.txt', 3) == expected


if __name__ == '__main__':
    print("Elf with most calories has: {}".format(count_calories('day01_real_input.txt')))
    print("Top 3 most calorie carrying elves have {}".format(count_calories('day01_real_input.txt', 3)))
