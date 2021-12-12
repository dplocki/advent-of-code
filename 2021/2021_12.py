START_CAVE = 'start'
EXIT_CAVE = 'end'


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> list[tuple[str, str]]:
    for line in task_input:
        _from, _to = line.split('-')

        yield _from, _to
        yield _to, _from


def is_cave_big(cave: str) -> bool:
    return cave.isupper()


def path_counter(task_input: list[tuple[str, str]], can_visit_cave: callable) -> int:


    def get_neighbors(caves_map: list[tuple[str, str]], from_where: str) -> list[str]:
        yield from set(_to for _from, _to in caves_map if from_where == _from and _to != START_CAVE)


    caves_map = list(parse(task_input))
    result = 0
    paths_to_analise = [[START_CAVE]]

    while paths_to_analise:
        current_path = paths_to_analise.pop()
        current_place = current_path[-1]

        if current_place == EXIT_CAVE:
            result += 1
            continue

        for neighborn in get_neighbors(caves_map, current_place):
            if can_visit_cave(neighborn, current_path):
                new_path = current_path.copy()
                new_path.append(neighborn)
                paths_to_analise.append(new_path)

    return result


def solution_for_first_part(task_input: list[tuple[str, str]]) -> int:
    visit_small_only_once = lambda cave, current_path: is_cave_big(cave) or cave not in current_path
    return path_counter(task_input, visit_small_only_once)


example_input_first = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''.splitlines()

example_input_second = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''.splitlines()

example_input_third = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''.splitlines()

assert solution_for_first_part(example_input_first) == 10
assert solution_for_first_part(example_input_second) == 19
assert solution_for_first_part(example_input_third) == 226

# The input is taken from: https://adventofcode.com/2021/day/12/input
task_input = list(load_input_file('input.12.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: list[tuple[str, str]]) -> int:


    def can_visit_again(cave: str, current_path: list[str]) -> bool:
        if cave not in current_path:
            return True

        only_small = [c for c in current_path if not is_cave_big(c)]
        return len(only_small) == len(set(only_small))


    visit_small_only_once_with_except = lambda cave, current_path: is_cave_big(cave) or can_visit_again(cave, current_path)
    return path_counter(task_input, visit_small_only_once_with_except)


assert solution_for_second_part(example_input_first) == 36
assert solution_for_second_part(example_input_second) == 103
assert solution_for_second_part(example_input_third) == 3509

print("Solution for the second part:", solution_for_second_part(task_input))
