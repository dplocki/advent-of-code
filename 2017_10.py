from functools import reduce


def twist_line(list, index, input):
    for i in range(int(input / 2)):
        first = (index + i) % len(list)
        second = (index + input - i - 1) % len(list)

        list[first], list[second] = list[second], list[first]

    return list


def hasher(circle_size: int, inputs: [int]):
    skip_size = 0
    index = 0
    list = [_ for _ in range(0, circle_size)]

    for input in inputs:
        result = twist_line(list, index, input)

        index += input + skip_size
        skip_size += 1
        yield result


def array_to_knot_hash(input: [int]) -> str:
    task_hasher = hasher(256, input * 64)

    result = [_ for _ in task_hasher][-1]
    splitted_results = [result[(x*16):(x*16+16)] for x in range(16)]
    dense_hash = [reduce(lambda x, y: x ^ y, splitted_result) for splitted_result in splitted_results]
    hex_hash = [('%x' % ch).zfill(2) for ch in dense_hash]

    return reduce(lambda x, y: x + y, hex_hash)


def string_to_knot_hash(input: str) -> str:
    return array_to_knot_hash([ord(c) for c in input] + [17, 31, 73, 47, 23])


if __name__ == '__main__':
    # Tests
    test_hasher = hasher(5, [3, 4, 1, 5])
    test_step_results = [
        [2, 1, 0, 3, 4],
        [4, 3, 0, 1, 2],
        [4, 3, 0, 1, 2],
        [3, 4, 2, 1, 0],
        [3, 4, 2, 1, 0]
    ]

    for test_set in zip(test_hasher, test_step_results):
        print(f'Assert: {test_set[0]} -> {test_set[1]}')
        assert test_set[0] == test_set[1]

    # Task
    input = [199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192]
    task_hasher = hasher(256, input)

    result = [_ for _ in task_hasher][-1]

    print("Solution for first part:", result[0] * result[1])
    print("Solution for second part:", string_to_knot_hash(','.join([str(_) for _ in input])))

    # Test of hasher
    assert string_to_knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert string_to_knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert string_to_knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert string_to_knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'
