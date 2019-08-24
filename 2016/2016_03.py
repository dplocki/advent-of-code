def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines):
    for line in lines:
        yield list(map(lambda x: int(x), line.split()))


def solution_for_first_part(input_list: [[int]]):
    result = 0

    for trinagle in input_list:
        trinagle.sort()
        if trinagle[2] < trinagle[0] + trinagle[1]:
            result += 1

    return result


# The input is taken from: https://adventofcode.com/2016/day/3/input
input_list = parse(load_input_file('input.03.txt'))
print("Solution for the first part:", solution_for_first_part(input_list))
