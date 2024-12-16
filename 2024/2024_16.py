from typing import Dict, Generator, Iterable, Tuple
import heapq


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Tuple[Dict[Tuple[int, int, str], int], Tuple[int, int], Tuple[int, int]]:
    maze = {(row, column): character
        for row, line in enumerate(task_input)
        for column, character in enumerate(line)}

    begin = None
    end = None
    for (poz, letter) in maze.items():
        if letter == 'S':
            begin = poz
        elif letter == 'E':
            end = poz

    maze[begin] = '.'
    maze[end] = '.'

    return maze, begin, end


def build_visiting_dictionary(maze: Dict[Tuple[int, int, str], int], start: Tuple[int, int]) -> Dict[Tuple[int, int, str], int]:
    to_checked = []
    heapq.heappush(to_checked, (0, (start, '>')))
    visited = { (start, '>') : 0 }

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

    return visited


def solution_for_first_part(task_input: Iterable[str]) -> int:
    maze, begin, end = parse(task_input)
    visited = build_visiting_dictionary(maze, begin)

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


def solution_for_second_part(task_input: Iterable[str]) -> int:
    maze, begin, end = parse(task_input)
    visited = build_visiting_dictionary(maze, begin)

    potential_sits = set()
    to_checked = [min(((end, '>'), (end, '^')), key=lambda p: visited[p])]

    while to_checked:
        location, direction = to_checked.pop()
        if (location, direction) not in visited:
            continue

        current_score = visited[location, direction]
        potential_sits.add(location)

        if direction == '^':
            directed_point = (location[0] + 1, location[1]), '^'
            if directed_point in visited and visited[directed_point] == current_score - 1:
                to_checked.append(directed_point)

            directed_point = (location[0] + 1, location[1]), '>'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

            directed_point = (location[0] + 1, location[1]), '<'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

        elif direction == 'v':
            directed_point = (location[0] - 1, location[1]), 'v'
            if directed_point in visited and visited[directed_point] == current_score - 1:
                to_checked.append(directed_point)

            directed_point = (location[0] - 1, location[1]), '>'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

            directed_point = (location[0] - 1, location[1]), '<'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

        elif direction == '>':
            directed_point = (location[0], location[1] - 1), '>'
            if directed_point in visited and visited[directed_point] == current_score - 1:
                to_checked.append(directed_point)

            directed_point = (location[0], location[1] - 1), '^'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

            directed_point = (location[0], location[1] - 1), 'v'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

        elif direction == '<':
            directed_point = (location[0], location[1] + 1), '<'
            if directed_point in visited and visited[directed_point] == current_score - 1:
                to_checked.append(directed_point)

            directed_point = (location[0], location[1] + 1), '^'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

            directed_point = (location[0], location[1] + 1), 'v'
            if directed_point in visited and visited[directed_point] == current_score - 1001:
                to_checked.append(directed_point)

        else:
            raise Exception('Incorrect state!')

    return len(potential_sits)


assert solution_for_second_part(smaller_example_input) == 45
assert solution_for_second_part(larger_example_input) == 64

print("Solution for the second part:", solution_for_second_part(task_input))