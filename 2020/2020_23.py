from itertools import islice, cycle, chain


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):
    return map(int, task_input)


def play(cups: [int], rounds: int) -> dict:
    connection_map = {cup:leading_to for cup, leading_to in zip(cups, islice(cycle(cups), 1, None))}
    last_cap = max(connection_map.keys())
    current = cups[0]

    for _ in range(rounds):
        first_away = connection_map[current]
        second_away = connection_map[first_away]
        third_away = connection_map[second_away]

        pick_up = (first_away, second_away, third_away)

        destination = current - 1
        while destination in pick_up or destination < 1:
            destination -= 1
            if destination < 1:
                destination = last_cap
        
        connection_map[current] = connection_map[third_away]
        connection_map[third_away] = connection_map[destination]
        connection_map[destination] = first_away

        current = connection_map[current]

    return connection_map


def solution_for_first_part(task_input):
    cups = list(parse(task_input))

    connection_map = play(cups, 100)

    result = []
    cup = connection_map[1]
    for i in range(1, 9):
        result.append(cup)
        cup = connection_map[cup]

    return ''.join(map(str, result))


assert solution_for_first_part('389125467') == '67384529'

# The input is taken from: https://adventofcode.com/2020/day/23/input
task_input = list(load_input_file('input.23.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):
    cups = list(chain(parse(task_input), range(len(task_input) + 1, 1_000_001)))
    connection_map = play(cups, 10_000_000)

    first = connection_map[1]
    second = connection_map[first]

    return first * second


assert solution_for_second_part('389125467') == 149245887792
print("Solution for the second part:", solution_for_second_part(task_input))
