def calculate_scanner_position(layer_lenght, time):
    position_table_length = layer_lenght * 2 - 2
    index_of_position = time % position_table_length

    if index_of_position < layer_lenght:
        return index_of_position

    return layer_lenght * 2 - index_of_position - 2


def test_of_calculate_scanner_position(layer_lenght, time, expected):
    result = calculate_scanner_position(layer_lenght, time)
    assert result == expected, f"Excepted: {expected}, recived: {result}"


test_of_calculate_scanner_position(3, 0, 0)
test_of_calculate_scanner_position(3, 1, 1)
test_of_calculate_scanner_position(3, 2, 2)
test_of_calculate_scanner_position(3, 3, 1)
test_of_calculate_scanner_position(3, 4, 0)
test_of_calculate_scanner_position(3, 5, 1)
test_of_calculate_scanner_position(3, 6, 2)
test_of_calculate_scanner_position(3, 7, 1)
test_of_calculate_scanner_position(3, 8, 0)


def find_scanners_on_index_zero(input, from_time):
    for k, v in input.items():
        if calculate_scanner_position(v, from_time + k) == 0:
            yield k, v


def calculate_severity(input, from_time: int = 0):
    result = 0

    for k, v in find_scanners_on_index_zero(input, from_time):
        result += v * k

    return result


def find_how_long_wait_for_clear_path(input: {}, time_from: int = 0):

    def is_path_clear(input: {}, time):
        for _, _ in find_scanners_on_index_zero(input, time):
            return False

        return True

    result = time_from
    while True:
        if is_path_clear(input, result):
            return result

        result += 1


test_input = {
    0: 3,
    1: 2,
    4: 4,
    6: 4
}

assert calculate_severity(test_input) == 24
assert calculate_severity(test_input, 10) == 0

input = {
    # get the content of https://adventofcode.com/2017/day/13/input and add the comas on end lines
}

print("Solution for the first part:", calculate_severity(input))
print("Solution for the second part:", find_how_long_wait_for_clear_path(input))
