def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def decode(line: str) -> (int, int):

    def find_number(low: int, hight: int, directions: [bool]) -> int:
        for direction in directions:
            size_of_group = (hight - low) // 2
            if direction:
                hight = low + size_of_group
            else:
                low = low + size_of_group + 1

        return low

    return (
        find_number(0, 127, [c == 'F' for c in line[:7]]),
        find_number(0, 7, [c == 'L' for c in line[7:]])
    )


def solution_for_first_part(lines: [str]) -> int:
    return max(
        row * 8 + column
        for row, column in (decode(line) for line in lines)
    )


assert decode('FBFBBFFRLR') == (44, 5)

# The input is taken from: https://adventofcode.com/2020/day/5/input
task_input = list(load_input_file('input.05.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
