def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def solution_for_the_first_part(lines: [str]):


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
            first = tokens[0]
            second = tokens[2]

            if tokens[1] == 'AND':
                return find_value_of(first, output_directory) & find_value_of(second, output_directory)
            if tokens[1] == 'OR':
                return find_value_of(first, output_directory) ^ find_value_of(second, output_directory)
            if tokens[1] == 'LSHIFT':
                return find_value_of(first, output_directory) << find_value_of(second, output_directory)
            if tokens[1] == 'RSHIFT':
                return find_value_of(first, output_directory) >> find_value_of(second, output_directory)
            else:
                raise "Uknown!"


    output_directory = build_output_directory(lines)
    return find_value_of(output_directory['a'], output_directory)


# The solution is taken from: https://adventofcode.com/2015/day/7/input
print("Solution for the first part:", solution_for_the_first_part(load_input_file('input.07.txt')))
