from typing import Generator, Iterable, Tuple
import heapq


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, int, str], None, None]:
    for row, line in enumerate(task_input):
        for column, character in enumerate(line):
            yield row, column, character


def solution_for_first_part(task_input: Iterable[str]) -> int:
    maze = { (row, column): letter for row, column, letter in parse(task_input) }
    begin = None
    end = None

    for (poz, letter) in maze.items():
        if letter == 'S':
            begin = poz
        elif letter == 'E':
            end = poz

    maze[begin] = '.'
    maze[end] = '.'

    to_checked = []
    heapq.heappush(to_checked, (0, (begin, '>')))
    visited = { (begin, '>') : 0 }

    while to_checked:
        score, (position, direction) = heapq.heappop(to_checked)

        if (position, direction) in visited and visited[position, direction] < score:
            continue

        visited[position, direction] = score

        if direction == '>':
            new_pos = position[0], position[1] + 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1, (new_pos, '>')))

            new_pos = position[0] + 1, position[1]
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, 'v')))

            new_pos = position[0] - 1, position[1]
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '^')))

        elif direction == '<':
            new_pos = position[0], position[1] - 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1, (new_pos, '<')))

            new_pos = position[0] + 1, position[1]
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, 'v')))

            new_pos = position[0] - 1, position[1]
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '^')))

        elif direction == '^':
            new_pos = position[0] - 1, position[1] + 0
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1, (new_pos, '^')))

            new_pos = position[0], position[1] + 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '>')))

            new_pos = position[0], position[1] - 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '<')))

        elif direction == 'v':
            new_pos = position[0] + 1, position[1] + 0
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1, (new_pos, 'v')))

            new_pos = position[0], position[1] + 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '>')))

            new_pos = position[0], position[1] - 1
            if maze[new_pos] == '.':
                heapq.heappush(to_checked, (score + 1001, (new_pos, '<')))

        else:
            raise Exception('Incorrect state!')

    return min(visited[end, '^'], visited[end, '>'])


smaller_example_input = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''.splitlines()

larger_example_input = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''.splitlines()


assert solution_for_first_part(smaller_example_input) == 7036
assert solution_for_first_part(larger_example_input) == 11048

# The input is taken from: https://adventofcode.com/2024/day/16/input
task_input = list(load_input_file('input.16.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
