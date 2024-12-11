import collections
from typing import Iterable


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def solution(how_many_blinks: int, task_input: Iterable[str]) -> int:
    stones = collections.Counter(task_input.split())

    for _ in range(how_many_blinks):
        new_stones = collections.Counter()

        for stone, how_many in stones.items():
            stone_number_length = len(stone)

            if stone == '0':
                new_stones['1'] += how_many
            elif stone_number_length % 2 == 0:
                new_stones[str(int(stone[:stone_number_length // 2]))] += how_many
                new_stones[str(int(stone[stone_number_length // 2:]))] += how_many
            else:
                new_stones[str(int(stone) * 2024)] += how_many

        stones = new_stones

    return sum(stones.values())


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return solution(25, task_input)


assert solution_for_first_part('125 17') == 55312

# The input is taken from: https://adventofcode.com/2024/day/11/input
task_input = load_input_file('input.11.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return solution(75, task_input)


print("Solution for the second part:", solution_for_second_part(task_input))