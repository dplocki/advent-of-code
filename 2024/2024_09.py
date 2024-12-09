from typing import Generator, Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def get_segment_from_left(blocks) -> Generator[Tuple[int, int], None, None]:
    index = 0

    for block_size, file_id in blocks:
        for _ in range(block_size):
            yield index, file_id
            index += 1


def get_file_segment_from_right(blocks) -> Generator[int, None, None]:
    for block_size, file_id in reversed(blocks):
        if file_id == None:
            continue

        for _ in range(block_size):
            yield file_id


def solution_for_first_part(task_input: Iterable[str]) -> int:
    blocks = [
        (int(block), block_index // 2 if block_index % 2 == 0 else None)
        for block_index, block in enumerate(task_input)
    ]

    last_left_index = sum(block_size for block_size, file_id in blocks if file_id != None) - 1
    result = 0
    left_index = 0
    any_segments_from_left = get_segment_from_left(blocks)
    file_segments_from_right = get_file_segment_from_right(blocks)

    while left_index != last_left_index:
        left_index, file_id = next(any_segments_from_left)
        if file_id == None:
            file_id = next(file_segments_from_right)

        result += left_index * file_id

    return result


example_input = '2333133121414131402'

assert solution_for_first_part(example_input) == 1928

# The input is taken from: https://adventofcode.com/2024/day/9/input
task_input = list(load_input_file('input.09.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
