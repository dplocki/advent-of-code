knot_hash = __import__('2017_10')


def count_used_square(input: str):
    digit_dictionary = {
        '{0:x}'.format(ch): '{0:b}'.format(ch).count('1')
        for ch in range(16)
    }

    result = 0
    for i in range(128):
        hash = knot_hash.string_to_knot_hash(f'{input}-{i}')

        for character in hash:
            result += digit_dictionary[character]

    return result


assert count_used_square('flqrgnkx') == 8108

print('Solution for first part:', count_used_square('jzgqcdpd'))
