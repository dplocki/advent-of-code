from typing import Dict, Generator, Iterable, Tuple


INDEX = 0
BLOCK_SIZE = 1
FILE_ID = 2


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Dict[int, Tuple[int, int, int]]:
    disc_structure = {}
    index = 0

    for block_index, block in enumerate(task_input):
        size = int(block)
        disc_structure[index] = (
            index,
            size,
            (block_index // 2) if block_index % 2 == 0 else None
        )

        index += size

    return disc_structure


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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    disc_structures = parse(task_input)
    ids = {
        structure[FILE_ID]: structure
        for structure in disc_structures.values()
        if structure[FILE_ID] != None
    }

    for file_id in range(len(ids) - 1, 0, -1):
        current_block = ids[file_id]

        for index in sorted(disc_structures.keys()):
            disc_structure = disc_structures[index]

            if index >= current_block[INDEX]:
                break

            if disc_structure[FILE_ID] != None:
                continue

            if current_block[BLOCK_SIZE] <= disc_structure[BLOCK_SIZE]:
                disc_structures[disc_structure[INDEX]] = (
                    disc_structure[INDEX],
                    current_block[BLOCK_SIZE],
                    current_block[FILE_ID],
                )

                different_size = disc_structure[BLOCK_SIZE] - current_block[BLOCK_SIZE]
                if different_size > 0:
                    disc_structures[disc_structure[INDEX] + current_block[BLOCK_SIZE]] = (
                        disc_structure[INDEX] + current_block[BLOCK_SIZE],
                        different_size,
                        None,
                    )

                disc_structures[current_block[INDEX]] = (
                    current_block[INDEX],
                    current_block[BLOCK_SIZE],
                    None,
                )
                break


    result = 0
    for key in sorted(disc_structures.keys()):
        block = disc_structures[key]

        if block[FILE_ID] == None:
            continue

        result += sum(
            (key + index) * block[FILE_ID]
            for index in range(block[BLOCK_SIZE]))

    return result

assert solution_for_second_part(example_input) == 2858
print("Solution for the second part:", solution_for_second_part(task_input))
