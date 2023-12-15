def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def hash(value: str) -> int:
    result = 0

    for character in value:
        result += ord(character)
        result *= 17
        result %= 256

    return result


def solution_for_first_part(task_input: str) -> int:
    return sum(map(hash, task_input.split(',')))


example_input = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

assert solution_for_first_part(example_input) == 1320

# The input is taken from: https://adventofcode.com/2023/day/15/input
task_input = load_input_file('input.15.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
