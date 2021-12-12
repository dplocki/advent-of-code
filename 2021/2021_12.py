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


def solution_for_first_part(task_input: list[tuple[str, str]]) -> int:


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
            if is_cave_big(neighborn) or neighborn not in current_path:
                p = current_path.copy()
                p.append(neighborn)
                paths_to_analise.append(p)

    return result


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
