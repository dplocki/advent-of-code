from collections import Counter
import itertools


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def find_twice_and_threes(input):
    values = Counter(input).values()

    return (2 in values, 3 in values)


assert find_twice_and_threes('abcdef') == (False, False)
assert find_twice_and_threes('bababc') == (True, True)
assert find_twice_and_threes('abbcde') == (True, False)
assert find_twice_and_threes('abcccd') == (False, True)
assert find_twice_and_threes('aabcdd') == (True, False)
assert find_twice_and_threes('abcdee') == (True, False)
assert find_twice_and_threes('ababab') == (False, True)


def count_twice_and_threes_for_list(list):
    twice_counter = 0
    threes_counter = 0

    for input in list:
        result = find_twice_and_threes(input)
        twice_counter += 1 if result[0] else 0
        threes_counter += 1 if result[1] else 0

    return twice_counter, threes_counter


test_input = ['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']
assert count_twice_and_threes_for_list(test_input) == (4, 3)


result = count_twice_and_threes_for_list(file_to_input_list('input.txt'))
print('Solution for first part:', result[0] * result[1])


def hamming_distance(input_a, input_b):
    return sum(a != b for a, b in zip(input_a, input_b))


def find_hamming_distance_equal_1(list):
    for a, b in itertools.combinations(list, 2):
        if hamming_distance(a, b) == 1:
            return a, b


second_part_test_input = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']

second_part_test_result = find_hamming_distance_equal_1(second_part_test_input)
assert second_part_test_result == ('fghij', 'fguij')


def strip_difference_from_strings(input_a, input_b):
    return ''.join(a for a, b in zip(input_a, input_b) if a == b)


assert strip_difference_from_strings(*second_part_test_result) == 'fgij'


result = strip_difference_from_strings(*find_hamming_distance_equal_1(file_to_input_list('input.txt')))
print('Solution for second part:', result)
