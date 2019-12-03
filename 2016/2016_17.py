import hashlib
from collections import deque


MAZE_SIZE = 4
LAST_COORDINATE = MAZE_SIZE - 1


def md5(from_string: str) -> str:
    return hashlib.md5(from_string.encode('utf-8')).hexdigest()


def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read()


def path_generator(passcode):

    def get_posibilities(point, path, passcode):
        x, y = point
        doors = list(map(lambda x: x in 'bcdef', md5(passcode + path)[:4]))

        #up, down, left, and right
        if y > 0 and doors[0]:
            yield (x, y - 1), path + 'U'

        if y < LAST_COORDINATE and doors[1]:
            yield (x, y + 1), path + 'D'

        if x > 0 and doors[2]:
            yield (x - 1, y), path + 'L'

        if x < LAST_COORDINATE and doors[3]:
            yield (x + 1, y), path + 'R'


    end = (LAST_COORDINATE, LAST_COORDINATE)
    posibilities = deque([((0, 0), '')])
    while posibilities:
        point, path = posibilities.popleft()

        if point == end:
            yield path
            continue

        for new_point, new_path in get_posibilities(point, path, passcode):
            posibilities.append((new_point, new_path))


def solution_for_first_part(passcode):
    return next(path_generator(passcode))


assert solution_for_first_part('ihgpwlah') == 'DDRRRD'
assert solution_for_first_part('kglvqrro') == 'DDUDRLRRUDRD'
assert solution_for_first_part('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

# The input is taken from: https://adventofcode.com/2016/day/17/input
passcode = load_input_file('input.17.txt')
print("Solution for the first part:", solution_for_first_part(passcode))


def solution_for_second_part(passcode):
    return max([len(i) for i in path_generator(passcode)])


assert solution_for_second_part('ihgpwlah') == 370
assert solution_for_second_part('kglvqrro') == 492
assert solution_for_second_part('ulqzkmiv') == 830

print("Solution for the second part:", solution_for_second_part(passcode))
