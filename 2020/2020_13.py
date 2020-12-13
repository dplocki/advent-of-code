def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: [str]):
    timestamp, buses = task_input.split('\n')
    return int(timestamp), (int(x) for x in buses.split(',') if x != 'x')


def solution_for_first_part(task_input):
    timestamp, buses = parse(task_input)
    earliest_bus = min(
        ((bus, ((timestamp // bus + 1) * bus) - timestamp) for bus in buses),
        key=lambda bus_with_arrive_time: bus_with_arrive_time[1]
    )

    return earliest_bus[0] * earliest_bus[1]


example_input = '''939
7,13,x,x,59,x,31,19'''

assert solution_for_first_part(example_input) == 295

# The input is taken from: https://adventofcode.com/2020/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


