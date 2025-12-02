from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input) -> Generator[Tuple[int, int], None, None]:
    for ranges in task_input.split(','):
        yield map(int, ranges.split('-'))


def solution_for_first_part(task_input: Iterable[Tuple[int, int]]) -> int:

    def internal() -> Generator[int, None, None]:
        for range_start, range_end in parse(task_input):
            for product_id in range(range_start, range_end + 1):
                id_as_string = str(product_id)
                id_len = len(id_as_string)

                if id_len % 2 == 1:
                    continue

                half_of_id_len = id_len >> 1
                if id_as_string[half_of_id_len:] == id_as_string[:half_of_id_len]:
                    yield product_id


    return sum(internal())


example_input = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124'''

assert solution_for_first_part(example_input) == 1227775554

# The input is taken from: https://adventofcode.com/2025/day/2/input
task_input = load_input_file('input.02.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
