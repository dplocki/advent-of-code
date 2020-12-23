def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):
    return map(int, task_input)


def solution_for_first_part(task_input):
    cups = list(parse(task_input))
    cups_len = len(cups)
    current_index = 0

    for _ in range(100):
        current = cups[current_index]
        double_cups = cups * 2
        pick_up = double_cups[current_index + 1:current_index + 4]

        destionation = current - 1
        while destionation in pick_up or destionation <= 0:
            if destionation <= 0:
                destionation = cups_len
            else:
                destionation -= 1

        rest_cups = double_cups[current_index + 4:current_index + 10]

        destionation_index = rest_cups.index(destionation)
        cups = rest_cups[:destionation_index + 1] + pick_up + rest_cups[destionation_index + 1:]

        current_index = (cups.index(current) + 1) % cups_len

    place_of_1 = cups.index(1)
    return ''.join(map(str, (cups[(place_of_1 + i) % cups_len] for i in range(1, 9))))


assert solution_for_first_part('389125467') == '67384529'

# The input is taken from: https://adventofcode.com/2020/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
