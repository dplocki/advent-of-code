def spinlock(step_lenght):
    iteration_number = 1

    memory = [0]
    index = 0

    while True:
        memory_lenght = len(memory)

        index = (index + step_lenght) % memory_lenght + 1
        if index > memory_lenght:
            memory.append(iteration_number)
        else:
            memory.insert(index, iteration_number)

        yield memory, index
        iteration_number += 1


def test_spinlock(result, expected):
    assert result == expected, "Excepted: {expected}, recived: {result}"


spinlock_test = spinlock(3)

test_spinlock(next(spinlock_test)[0], [0, 1])
test_spinlock(next(spinlock_test)[0], [0, 2, 1])
test_spinlock(next(spinlock_test)[0], [0, 2, 3, 1])

test_spinlock(next(spinlock_test)[0], [0, 2, 4, 3, 1])
test_spinlock(next(spinlock_test)[0], [0, 5, 2, 4, 3, 1])
test_spinlock(next(spinlock_test)[0], [0, 5, 2, 4, 3, 6, 1])
test_spinlock(next(spinlock_test)[0], [0, 5, 7, 2, 4, 3, 6, 1])
test_spinlock(next(spinlock_test)[0], [0, 5, 7, 2, 4, 3, 8, 6, 1])
test_spinlock(next(spinlock_test)[0], [0, 9, 5, 7, 2, 4, 3, 8, 6, 1])


def solution_for(steps):
    result = None
    for memory, _ in zip(spinlock(steps), range(2017)):
        result = memory

    return result[0][result[1] + 1]


assert solution_for(3) == 638


print('Solution for first part:', solution_for(343))
