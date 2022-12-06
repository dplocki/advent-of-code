def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def solution_for_first_part(task_input: str) -> int:
    PACKAGE_SIZE = 4

    for index in range(len(task_input) - PACKAGE_SIZE):
        if len(set(task_input[index:index + PACKAGE_SIZE])) == PACKAGE_SIZE:
            return index + PACKAGE_SIZE


assert solution_for_first_part('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert solution_for_first_part('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert solution_for_first_part('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert solution_for_first_part('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert solution_for_first_part('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11


# The input is taken from: https://adventofcode.com/2022/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
