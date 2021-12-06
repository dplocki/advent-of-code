from typing import List


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: List[str]):
    return map(int, task_input.split(','))


def solution_for_first_part(task_input):
    fishes = list(parse(task_input))

    for _ in range(80):
        new_fishes = []
        for fish in fishes:
            if fish == 0:
                new_fishes.append(6)
                new_fishes.append(8)
            else:
                new_fishes.append(fish - 1)

        fishes = new_fishes

    return len(new_fishes)


example_input = '''3,4,3,1,2'''

assert solution_for_first_part(example_input) == 5934

# The input is taken from: https://adventofcode.com/2021/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
