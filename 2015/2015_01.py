def what_floor(input: str):
    return input.count('(') - input.count(')')


def position_of_first_basement(input: str):
    floor = 0

    for index, character in enumerate(input):
        if character == '(':
            floor += 1
        elif character == ')':
            floor -= 1

            if floor < 0:
                return index + 1


assert what_floor('(())') == 0
assert what_floor('()()') == 0
assert what_floor('(((') == 3
assert what_floor('(()(()(') == 3
assert what_floor('))(((((') == 3
assert what_floor('())') == -1
assert what_floor('))(') == -1

assert what_floor(')))') == -3
assert what_floor(')())())') == -3


assert position_of_first_basement(')') == 1
assert position_of_first_basement('()())') == 5


# The input taken from: https://adventofcode.com/2015/day/1/input
with open('input.1.txt', 'r') as file:
    input = file.read()

    print("Solution for the first part:", what_floor(input))
    print("Solution for the second part:", position_of_first_basement(input))
