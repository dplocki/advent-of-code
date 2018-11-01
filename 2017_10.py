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

new_inputs = [ord(c) for c in ','.join([str(_) for _ in input])] + [17, 31, 73, 47, 23]
task_hasher = hasher(256, new_inputs * 64)

result = [_ for _ in task_hasher][-1]

from functools import reduce

splitted_results = [result[(x*16):(x*16+16)] for x in range(16)]
dense_hash = [reduce(lambda x, y: x ^ y, splitted_result) for splitted_result in splitted_results]
hex_hash = [('%x' % ch).zfill(2) for ch in dense_hash]

print("Solution for second part:", reduce(lambda x, y: x + y, hex_hash))
