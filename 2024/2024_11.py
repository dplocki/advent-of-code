from typing import Iterable


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def solution_for_first_part(task_input: Iterable[str]) -> int:
    stones = task_input.split()

    for _ in range(25):
        new_stones = []

        for stone in stones:
            if stone == '0':
                new_stones.append('1')
            elif len(stone) % 2 == 0:
                new_stones.append(str(int(stone[:len(stone) // 2])))
                new_stones.append(str(int(stone[len(stone) // 2:])))
            else:
                new_stones.append(str(int(stone) * 2024))

        stones = new_stones

    return len(stones)


example_input = '125 17'

assert solution_for_first_part(example_input) == 55312

# The input is taken from: https://adventofcode.com/2024/day/11/input
task_input = load_input_file('input.11.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
