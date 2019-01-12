knot_hash = __import__('2017_10')


def input_to_hash_list(input) -> [[str]]:
    return [
        knot_hash.string_to_knot_hash(f'{input}-{i}')
        for i in range(128)
    ]


def count_used_square(input: str):
    digit_dictionary = {
        '{0:x}'.format(ch): '{0:b}'.format(ch).count('1')
        for ch in range(16)
    }

    result = 0
    for hash in input_to_hash_list(input):
        for character in hash:
            result += digit_dictionary[character]

    return result


def input_to_2d_array(input):
    digit_dictionary = {
        '{0:x}'.format(ch): '{0:b}'.format(ch).zfill(4)
        for ch in range(16)
    }

    result = []
    for hash in input_to_hash_list(input):
        line = []
        for character in hash:
            line += [0 if r == '0' else -1 for r in digit_dictionary[character]]

        result.append(line)

    return result


def mark_group(_2d_array: [[int]], x: int, y: int, group_number: int):
    if x >= 0 and x < 128 and y >= 0 and y < 128 and _2d_array[x][y] == -1:
        _2d_array[x][y] = group_number

        mark_group(_2d_array, x, y - 1, group_number)
        mark_group(_2d_array, x - 1, y, group_number)
        mark_group(_2d_array, x + 1, y, group_number)
        mark_group(_2d_array, x, y + 1, group_number)


def count_all_groups(input: str) -> int:
    _2d_array = input_to_2d_array(input)

    group_number = 0
    for x in range(128):
        for y in range(128):
            if _2d_array[x][y] == -1:
                group_number += 1
                mark_group(_2d_array, x, y, group_number)


    return group_number


assert count_used_square('flqrgnkx') == 8108
assert count_all_groups('flqrgnkx') == 1242

print('Solution for first part:', count_used_square('jzgqcdpd'))
print('Solution for second part:', count_all_groups('jzgqcdpd'))
