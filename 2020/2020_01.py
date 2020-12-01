SUM = 2020

def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)

def solution_for_first_part(task_input: [int]) -> int:
    for value in task_input:
        other_value = SUM - value
        if other_value in task_input:
            return value * other_value


assert solution_for_first_part([1721, 979, 366, 299, 675, 1456]) == 514579

# The input is taken from: https://adventofcode.com/2020/day/1/input
task_input = list(load_input_file('input.01.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
