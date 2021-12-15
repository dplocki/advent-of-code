from queue import PriorityQueue


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[int, int, int]]:
    for row_index, row in enumerate(task_input):
        for column_index, value in enumerate(row):
            yield column_index, row_index, int(value)


def get_four_neighbors(x: int, y: int) -> tuple[int, int]:
    yield x, y - 1 # NORTH
    yield x + 1, y # EAST
    yield x, y + 1 # SOUTH
    yield x - 1, y # WEST


def heuristic(current_point: tuple[int, int], target: tuple[int, int]) -> int:
    return abs(current_point[0] - target[0]) + abs(current_point[1] - target[1])


def get_neighborns(risk_map: dict[tuple[int, int], int], current: tuple[int, int]) -> list[tuple[int, int]]:
    yield from (neighbor for neighbor in get_four_neighbors(*current) if neighbor in risk_map)


def solution_for_first_part(task_input: list[str]) -> int:
    risk_map = {(x,y): risk for x, y, risk in parse(task_input)}
    
    end_x = max(x for x, _ in risk_map.keys())
    end_y = max(y for _, y in risk_map.keys())

    start_point = (0, 0)
    target = (end_x, end_y)

    frontier = PriorityQueue()
    frontier.put((0, start_point))

    cost_so_far = {start_point: 0}

    while not frontier.empty():
        current = frontier.get()[1]
        if current == target:
            return cost_so_far[current]

        for next in get_neighborns(risk_map, current):
            new_cost = cost_so_far[current] + risk_map[next]

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, target)
                frontier.put((priority, next))

    raise Exception("no path found")


example_input = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''.splitlines()

assert solution_for_first_part(example_input) == 40

# The input is taken from: https://adventofcode.com/2021/day/15/input
task_input = list(load_input_file('input.15.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
