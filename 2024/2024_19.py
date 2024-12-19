from typing import Iterable, Tuple
from functools import lru_cache


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[Iterable[str], Iterable[str]]:
    raw_towels, raw_designs = task_input.split('\n\n')

    return tuple(token for token in raw_towels.split(', ')), tuple(line for line in raw_designs.splitlines())


def solution(task_input: Iterable[str]) -> int:
    towels, designs = parse(task_input)

    @lru_cache
    def count_design_realizations(target: str) -> int:
        if target == '':
            return 1

        return sum(count_design_realizations(target[len(towel):])
            for towel in towels
            if target.startswith(towel))

    return {
        design:count_design_realizations(design)
        for design in designs
    }


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(1 for value in solution(task_input).values() if value > 0)


example_input = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb'''

assert solution_for_first_part(example_input) == 6

# The input is taken from: https://adventofcode.com/2024/day/19/input
task_input = load_input_file('input.19.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    return sum(solution(task_input).values())


assert solution_for_second_part(example_input) == 16
print("Solution for the second part:", solution_for_second_part(task_input))
