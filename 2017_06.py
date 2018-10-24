def redistribution_step(bank):
    bank_len = len(bank)

    the_biggest_value = max(bank) 
    index_of_biggest = bank.index(the_biggest_value)
    bank[index_of_biggest] = 0

    for i in range(the_biggest_value):
        to_index = (index_of_biggest + i + 1) % bank_len
        bank[to_index] += 1

    return bank

def find_steps_for_cicle(bank):
    memory = []
    steps = 1

    while True:
        result = redistribution_step(bank)
        _hash = ':'.join(str(x) for x in result)

        if _hash not in memory:
            memory.append(_hash)
        else:
            return steps

        steps += 1


result = redistribution_step([0, 2, 7, 0])
assert result == [2, 4, 1, 2]

result = redistribution_step([2, 4, 1, 2])
assert result == [3, 1, 2, 3]

result = redistribution_step([3, 1, 2, 3])
assert result == [0, 2, 3, 4]

result = find_steps_for_cicle([0, 2, 7, 0])
assert result == 5

# Calculate the result
print(find_steps_for_cicle([4, 10, 4, 1, 8, 4, 9, 14, 5, 1, 14, 15, 0, 15, 3, 5]))
