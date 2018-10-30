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

task_hasher = hasher(256, [199,0,255,136,174,254,227,16,51,85,1,2,22,17,7,192])

result = None
for _ in task_hasher:
    result = _

print("Solution: ", result[0] * result[1])
