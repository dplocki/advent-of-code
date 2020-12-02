import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    pattern = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')

    for line in lines:
        groups = pattern.match(line)
        yield int(groups[1]), int(groups[2]), groups[3], groups[4]


def count_matching_policies(task_input, check_policy):
    policies = parse(task_input)

    return sum(1 for _ in filter(check_policy, policies))


def solution_for_first_part(task_input):

    def check_policy(policy):
        minium, maximum, letter, password = policy
        letter_count = password.count(letter)

        return minium <= letter_count <= maximum

    return count_matching_policies(task_input, check_policy)


assert solution_for_first_part('''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''.splitlines()) == 2

# The input is taken from: https://adventofcode.com/2020/day/2/input
task_input = list(load_input_file('input.02.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input):

    def check_policy(policy):
        first_position, second_position, letter, password = policy
        password_length = len(password)
        first_character = password[first_position - 1] if first_position <= password_length else None
        second_character = password[second_position - 1] if second_position <= password_length else None

        return bool(first_character == letter) ^ bool(second_character == letter)

    return count_matching_policies(task_input, check_policy)


assert solution_for_second_part('''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''.splitlines()) == 1

print("Solution for the second part:", solution_for_second_part(task_input))
