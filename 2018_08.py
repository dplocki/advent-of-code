def input_generator(input: str):
    for i in [int(i) for i in input.split(' ')]:
        yield i


def get_meta_data_sum(input: [int]) -> int:
    result = 0
    children = next(input)
    metadata = next(input)

    for _ in range(children):
        result += get_meta_data_sum(input)

    for _ in range(metadata):
        result += next(input)

    return result


assert get_meta_data_sum(input_generator('0 1 99')) == 99
assert get_meta_data_sum(input_generator('0 3 10 11 12')) == 33
assert get_meta_data_sum(input_generator('1 1 0 1 99 2')) == 101
assert get_meta_data_sum(input_generator('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2')) == 138

# The input taken from https://adventofcode.com/2018/day/8/input
input = '<input>'
print('Solution for first part:', get_meta_data_sum(input_generator(input)))
