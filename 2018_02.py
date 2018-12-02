from collections import Counter


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line


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
