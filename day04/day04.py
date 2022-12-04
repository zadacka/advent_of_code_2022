def complete_overlap(set1, set2):
    return set1.issubset(set2) or set2.issubset(set1)


def partial_overlap(set1, set2):
    return len(set1.intersection(set2)) > 0


def region_to_set(region):
    start, end = [int(x) for x in region.split('-')]
    return set(range(start, end + 1))


def calculate_overlapping_pairs(input_filename, overlap_comparison):
    overlapping_regions = 0
    with open(input_filename) as f:
        for pair in f.readlines():
            region1, region2 = pair.strip().split(',')
            set1 = region_to_set(region1)
            set2 = region_to_set(region2)
            if overlap_comparison(set1, set2):
                overlapping_regions += 1
    return overlapping_regions


def test__overlap():
    assert complete_overlap(region_to_set("2-8"), region_to_set("3-7")) is True
    assert complete_overlap(region_to_set("2-8"), region_to_set("3-7")) is True
    assert complete_overlap(region_to_set("6-6"), region_to_set("2-6")) is True
    assert complete_overlap(region_to_set("6-6"), region_to_set("7-8")) is False
    # ^ ... had a bug here - was getting an 'always subset' empty set for n-n


def test__part1():
    assert calculate_overlapping_pairs('day04_test_input.txt', complete_overlap) == 2
    assert calculate_overlapping_pairs('day04_real_input.txt', complete_overlap) == 498


def test__part2():
    assert calculate_overlapping_pairs('day04_test_input.txt', partial_overlap) == 4
    assert calculate_overlapping_pairs('day04_real_input.txt', partial_overlap) == 859
