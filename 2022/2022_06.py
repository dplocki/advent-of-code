def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def solution(task_input: str, how_many_distinct: int) -> int:
    for index in range(len(task_input) - how_many_distinct):
        if len(set(task_input[index:index + how_many_distinct])) == how_many_distinct:
            return index + how_many_distinct


def solution_for_first_part(task_input: str) -> int:
    return solution(task_input, 4)


assert solution_for_first_part('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert solution_for_first_part('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert solution_for_first_part('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert solution_for_first_part('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert solution_for_first_part('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

# The input is taken from: https://adventofcode.com/2022/day/6/input
task_input = load_input_file('input.06.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:
    return solution(task_input, 14)


assert solution_for_second_part('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19
assert solution_for_second_part('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23
assert solution_for_second_part('nppdvjthqldpwncqszvftbrmjlhg') == 23
assert solution_for_second_part('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29
assert solution_for_second_part('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26

print("Solution for the second part:", solution_for_second_part(task_input))
