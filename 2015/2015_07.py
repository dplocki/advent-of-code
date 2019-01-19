def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def build_output_directory(lines: [str]):
    result = {}
    for line in lines:
        tmp = line.split(' -> ', 1)

        left_part = tmp[0]
        right_part = tmp[1]
        result[right_part] = left_part

    return result


def find_value_of(value, output_directory: {}) -> int:
    if not isinstance(value, str):
        return value
    elif value.isdigit():
        return int(value)
    elif ' ' not in value:
        tmp = find_value_of(output_directory[value], output_directory)
        output_directory[value] = tmp
        return tmp
    elif 'NOT' in value:
        return ~find_value_of(value.replace('NOT ', ''), output_directory)
    else:
        tokens = value.split(' ')
        first, second = tokens[0], tokens[2]

        if tokens[1] == 'AND':
            return find_value_of(first, output_directory) & find_value_of(second, output_directory)
        if tokens[1] == 'OR':
            return find_value_of(first, output_directory) ^ find_value_of(second, output_directory)
        if tokens[1] == 'LSHIFT':
            return find_value_of(first, output_directory) << find_value_of(second, output_directory)
        if tokens[1] == 'RSHIFT':
            return find_value_of(first, output_directory) >> find_value_of(second, output_directory)
        else:
            raise "Unknown!"


def solution_for_the_first_part(output_directory: {}):
    return find_value_of(output_directory['a'], output_directory)


def solution_for_the_second_part(output_directory: {}, result_of_first_part: int):
    output_directory['b'] = result_of_first_part
    return find_value_of(output_directory['a'], output_directory)


# The solution is taken from: https://adventofcode.com/2015/day/7/input
output_directory = build_output_directory(load_input_file('input.07.txt'))
a_wire_value = solution_for_the_first_part(output_directory.copy())

print("Solution for the first part:", a_wire_value)
print("Solution for the second part:", solution_for_the_second_part(output_directory, a_wire_value))
