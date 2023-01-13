from typing import Callable, Dict, Generator, Iterable, Set, Tuple, Union


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


def solution(board_map: Dict[Tuple[int, int], str], instructions: Iterable[Union[str, int]], wrap_coordinates: Callable[[Dict[Tuple[int, int], str], int, int, int], Tuple[int, int]]) -> int:
    current_row = 1
    current_column = min(column for row, column in board_map.keys() if row == 1)
    current_facing = 0 # right
    facing = 0 

    for instruction in instructions:
        if instruction == 'L':
            current_facing = (current_facing - 1) % 4
        elif instruction == 'R':
            current_facing = (current_facing + 1) % 4
        else:
            for _ in range(instruction, 0, -1):
                y, x = current_row, current_column

                if current_facing == 0:
                    x = current_column + 1
                elif current_facing == 2:
                    x = current_column - 1
                elif current_facing == 1:
                    y = current_row + 1
                elif current_facing == 3:
                    y = current_row - 1

                if (y, x) not in board_map:
                    y, x, facing = wrap_coordinates(y, x, current_facing)
                else:
                    facing = current_facing

                if board_map[y, x] == '#':
                    break
                else:
                    current_row = y
                    current_column = x
                    current_facing = facing
                    instruction -= 1

    return 1000 * current_row + 4 * current_column + current_facing


def solution_for_first_part(task_input: Iterable[str]) -> int:


    def wrap_coordinates(board_map: Dict[Tuple[int, int], str], y: int, x: int, facing: int) -> Tuple[int, int]:
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
                return y, x, facing

            y, x = current_y, current_x


    board_map, instructions = parse(task_input)

    return solution(board_map, instructions, lambda row, column, facing: wrap_coordinates(board_map, row, column, facing))


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


def solution_for_second_part(task_input: Iterable[str]) -> int:


    def create_mapping(border_points: Set[Tuple[int, int]], first_point: Tuple[int, int], first_direction: Tuple[int, int], second_point: Tuple[int, int], second_direction: Tuple[int, int]):
        is_first_turning = False
        is_second_turning = False

        while not(is_first_turning and is_second_turning):
            yield first_point, first_direction[0] != 0, second_point, second_direction[0] != 0

            first_tmp = first_point[0] + first_direction[0], first_point[1] + first_direction[1]
            second_tmp = second_point[0] + second_direction[0], second_point[1] + second_direction[1]

            if first_tmp in border_points:
                first_point = first_tmp
                is_first_turning = False
            else:
                if (first_point[0] - 1, first_point[1]) in border_points and first_direction[0] != 1:
                    first_direction = -1, 0
                elif (first_point[0] + 1, first_point[1]) in border_points and first_direction[0] != -1:
                    first_direction = 1, 0
                elif (first_point[0], first_point[1] - 1) in border_points and first_direction[1] != 1:
                    first_direction = 0, -1
                elif (first_point[0], first_point[1] + 1) in border_points and first_direction[1] != -1:
                    first_direction = 0, 1
                else:
                    raise Exception('something wrong')

                is_first_turning = True

            if second_tmp in border_points:
                second_point = second_tmp
                is_second_turning = False
            else:
                if (second_point[0] - 1, second_point[1]) in border_points and second_direction[0] != 1:
                    second_direction = -1, 0
                elif (second_point[0] + 1, second_point[1]) in border_points and second_direction[0] != -1:
                    second_direction = 1, 0
                elif (second_point[0], second_point[1] - 1) in border_points and second_direction[1] != 1:
                    second_direction = 0, -1
                elif (second_point[0], second_point[1] + 1) in border_points and second_direction[1] != -1:
                    second_direction = 0, 1
                else:
                    raise Exception('something wrong')

                is_second_turning = True


    def build_wrap_map(board_map: Dict[Tuple[int, int], str]):


        def find_facing(board_map: Dict[Tuple[int, int], str], point: Tuple[int, int], is_vertical: bool) -> int:
            if is_vertical:
                return (2, 0) if (point[0], point[1] - 1) in board_map else (0, 2)

            return (3, 1) if (point[0] - 1, point[1]) in board_map else (1, 3)


        def find_folding_starting_point(board_map: Dict[Tuple[int, int], str]) -> Generator[Tuple[int, int], None, None]:
            check_points = [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 1), (1, 0), (0, -1), (-1, 0)]
            for point_y, point_x in board_map.keys():
                if sum(1 for y, x in check_points if (point_y + y, point_x + x) in board_map) == 7:
                    yield point_y, point_x


        CHECK_POINTS = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        result = {}
        border_points = set(
            (y, x)
            for y, x in board_map.keys()
            if not ((y + 1, x) in board_map \
                and (y - 1, x) in board_map \
                and (y, x + 1) in board_map \
                and (y, x - 1) in board_map))

        for start_y, start_x in find_folding_starting_point(board_map):
            direction_y, direction_x = next((y, x) for y, x in CHECK_POINTS if (start_y + y, start_x + x) not in board_map)
        
            for first_point, is_first_vertical, second_point, is_second_vertical in create_mapping(border_points,
                (start_y + direction_y, start_x), (direction_y, 0),
                (start_y, start_x + direction_x), (0, direction_x)):

                first_facing = find_facing(board_map, first_point, is_first_vertical)
                second_facing = find_facing(board_map, second_point, is_second_vertical)

                result[first_point[0], first_point[1], first_facing[1]] = second_point[0], second_point[1], second_facing[0]
                result[second_point[0], second_point[1], second_facing[1]] = first_point[0], first_point[1], first_facing[0]

        return result


    def wrap_coordinates(wrap_map: Dict[Tuple[int, int, int], Tuple[int, int, int]], row: int, column: int, facing: int):
        match facing:
            case 0:
                return wrap_map[row, column - 1, facing]
            case 1:
                return wrap_map[row - 1, column, facing]
            case 2:
                return wrap_map[row, column + 1, facing]
            case 3:
                return wrap_map[row + 1, column, facing]

        raise Exception('Unknown value')


    board_map, instructions = parse(task_input)
    wrap_map = build_wrap_map(board_map)

    return solution(board_map, instructions, lambda row, column, facing: wrap_coordinates(wrap_map, row, column, facing))


assert solution_for_second_part(example_input) == 5031
print("Solution for the second part:", solution_for_second_part(task_input))
