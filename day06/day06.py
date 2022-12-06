def find_marker(input_string, distinct_chars=4):
    end_position = len(input_string) - distinct_chars - 1
    for index in range(end_position):
        chunk = slice(index, index + distinct_chars)
        four_character_chunk = input_string[chunk]
        if len(set(four_character_chunk)) == distinct_chars:
            return index + distinct_chars


def test__find_marker():
    assert 7 == find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    assert 5 == find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz")
    assert 6 == find_marker("nppdvjthqldpwncqszvftbrmjlhg")
    assert 10 == find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    assert 11 == find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")

    assert 19 == find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", distinct_chars=14)
    assert 23 == find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", distinct_chars=14)
    assert 23 == find_marker("nppdvjthqldpwncqszvftbrmjlhg", distinct_chars=14)
    assert 29 == find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", distinct_chars=14)
    assert 26 == find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", distinct_chars=14)


def test__parts_1_and_2():
    with open('day06_real_input.txt') as f:
        input_text = f.read()

    assert 1210 == find_marker(input_text)
    assert 3476 == find_marker(input_text, distinct_chars=14)
