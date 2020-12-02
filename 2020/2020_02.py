import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    pattern = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')

    for line in lines:
        groups = pattern.match(line)
        yield int(groups[1]), int(groups[2]), groups[3], groups[4]


def solution_for_first_part(task_input):

    def check_policy(policy):
        minium, maximum, letter, password = policy
        letter_count = password.count(letter)

        return minium <= letter_count <= maximum


    policies = parse(task_input)
    return sum(1 for _ in filter(check_policy, policies))


assert solution_for_first_part('''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''.splitlines()) == 2

# The input is taken from: https://adventofcode.com/2020/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
