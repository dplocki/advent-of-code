MESSAGE_LENGTH = 8


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def calculate_the_letter_occurents(input_lines: [str]) -> [dict]:
    result = [{} for _ in range(MESSAGE_LENGTH)]

    for input_line in input_lines:
        for index, value in enumerate(input_line):
            result[index][value] = result[index].get(value, 0) + 1

    return result


def get_the_most_common_letter(position_occurent: [dict]):
    for position_occurent in position_occurent:
        yield max(position_occurent, key=position_occurent.get)


def get_the_least_common_letter(position_occurent: [dict]):
    for position_occurent in position_occurent:
        yield min(position_occurent, key=position_occurent.get)


def solution_for_first_part(input: [str]) -> str:
    return ''.join(get_the_most_common_letter(calculate_the_letter_occurents(input)))


def solution_for_second_part(input: [str]) -> str:
    return ''.join(get_the_least_common_letter(calculate_the_letter_occurents(input)))


# The input is taken from: https://adventofcode.com/2016/day/6/input
input = list(load_input_file('input.06.txt'))
print("Solution for the first part:", solution_for_first_part(input))
print("Solution for the second part:", solution_for_second_part(input))
