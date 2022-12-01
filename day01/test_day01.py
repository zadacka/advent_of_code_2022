from day01.day01 import count_calories


def test__calorie_count():
    expected = 24000
    assert count_calories('day01_test_input.txt') == expected


def test__top_three_calorie_count():
    expected = 45000
    assert count_calories('day01_test_input.txt', 3) == expected
