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


def get_root_node(input: [int]) -> int:
    result = 0
    children = next(input)
    metadata = next(input)

    if children == 0:
        for _ in range(metadata):
            result += next(input)
    else:
        children_roots = [get_root_node(input) for _ in range(children)]

        for _ in range(metadata):
            meta = next(input) - 1

            result += children_roots[meta] if meta < children else 0

    return result


def test_root_node(input: str, excepted):
    result = get_root_node(input_generator(input))

    assert result == excepted, f"Except: {excepted} recived: {result}"


test_root_node('0 1 99', 99)
test_root_node('0 3 10 11 12', 33)
test_root_node('1 1 0 1 99 2', 0)
test_root_node('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2', 66)


print('Solution for second part:', get_root_node(input_generator(input)))
