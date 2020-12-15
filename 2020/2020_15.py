def load_input_file(file_name: str) -> str:

    def parse(task_input: [str]):
        yield from map(int, task_input.split(','))


    with open(file_name) as file:
        return parse(file.read().strip())


def simulator(max_turn, task_input):
    pre_history = {}
    history = {number:i for i, number in enumerate(task_input)}
    last_number_spoken = task_input[-1]

    for turn in range(len(task_input), max_turn):
        last_number_spoken = history[last_number_spoken] - pre_history.get(last_number_spoken, turn)
        if last_number_spoken <= 0:
            last_number_spoken = 0

        pre_history[last_number_spoken] = history.get(last_number_spoken, turn)
        history[last_number_spoken] = turn

    return last_number_spoken


def solution_for_first_part(task_input: [int]):
    return simulator(2020, task_input)


assert solution_for_first_part([0, 3, 6]) == 436
assert solution_for_first_part([1, 3, 2]) == 1
assert solution_for_first_part([2, 1, 3]) == 10
assert solution_for_first_part([1, 2, 3]) == 27
assert solution_for_first_part([2, 3, 1]) == 78
assert solution_for_first_part([3, 2, 1]) == 438
assert solution_for_first_part([3, 1, 2]) == 1836

# The input is taken from: https://adventofcode.com/2020/day/15/input
task_input = list(load_input_file('input.15.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: [int]):
    return simulator(30000000, task_input)


assert solution_for_second_part([0, 3, 6]) == 175594
assert solution_for_second_part([1, 3, 2]) == 2578
assert solution_for_second_part([2, 1, 3]) == 3544142
assert solution_for_second_part([1, 2, 3]) == 261214
assert solution_for_second_part([2, 3, 1]) == 6895259
assert solution_for_second_part([3, 2, 1]) == 18
assert solution_for_second_part([3, 1, 2]) == 362

print("Solution for the second part:", solution_for_second_part(task_input))
