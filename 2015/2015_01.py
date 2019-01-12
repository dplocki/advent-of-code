def what_floor(input: str):
    return input.count('(') - input.count(')')


assert what_floor('(())') == 0
assert what_floor('()()') == 0
assert what_floor('(((') == 3
assert what_floor('(()(()(') == 3
assert what_floor('))(((((') == 3
assert what_floor('())') == -1
assert what_floor('))(') == -1

assert what_floor(')))') == -3
assert what_floor(')())())') == -3


# The input taken from: https://adventofcode.com/2015/day/1/input
with open('input.1.txt', 'r') as file:
    input = file.read()

    print("Solution for the first part:", what_floor(input))
