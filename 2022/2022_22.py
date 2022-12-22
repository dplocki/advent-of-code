from typing import Dict, Generator, Iterable, Tuple, Union


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int], str], Generator[Generator[Union[int, str], None, None], None, None]]:

    def parse_path(path: str) -> Generator[Union[int, str], None, None]:
        tokens = path.replace('L', ' L ').replace('R', ' R ').split(' ')

        for token in tokens:
            yield token if token in 'RL' else int(token)


    def parse_board(raw_board: str) -> Dict[Tuple[int, int], str]:
        return {(row + 1, column + 1): character
        for row, line in enumerate(raw_board.splitlines())
        for column, character in enumerate(line)
        if character != ' '}


    raw_board, path = task_input.split('\n\n')
    return parse_board(raw_board), parse_path(path)


def wrap_coordinates(board_map: Dict[Tuple[int, int], str], facing: int, y: int, x: int) -> Tuple[int, int]:
    while True:
        current_y, current_x = y, x

        if facing == 0:
            current_x -= 1
        elif facing == 2:
            current_x += 1
        elif facing == 1:
            current_y -= 1
        elif facing == 3:
            current_y += 1

        if (current_y, current_x) not in board_map:
            return y, x

        y, x = current_y, current_x


def solution_for_first_part(task_input: Iterable[str]) -> int:
    board_map, instructions = parse(task_input)

    current_row = 1
    current_column = min(column for row, column in board_map.keys() if row == 1)
    facing = 0 # right

    for instruction in instructions:
        if instruction == 'L':
            facing = (facing - 1) % 4
        elif instruction == 'R':
            facing = (facing + 1) % 4
        else:
            for _ in range(instruction, 0, -1):
                y, x = current_row, current_column

                if facing == 0:
                    x = current_column + 1
                elif facing == 2:
                    x = current_column - 1
                elif facing == 1:
                    y = current_row + 1
                elif facing == 3:
                    y = current_row - 1

                if (y, x) not in board_map:
                    y, x = wrap_coordinates(board_map, facing, y, x)

                if board_map[y, x] == '#':
                    break
                else:
                    current_row = y
                    current_column = x
                    instruction -= 1

    return 1000 * current_row + 4 * current_column + facing


example_input = '''        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5'''

assert solution_for_first_part(example_input) == 6032

# The input is taken from: https://adventofcode.com/2022/day/22/input
task_input = load_input_file('input.22.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
