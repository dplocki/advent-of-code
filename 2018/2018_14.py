from collections import deque


def state_generator():
    state = [3, 7]
    first_elf_index = 0
    second_elf_index = 1

    yield state[0]
    yield state[1]

    while True:
        new_recipe = state[first_elf_index] + state[second_elf_index]
        
        if new_recipe >= 10:
            first_recipe = int(new_recipe / 10)
            second_recipe = new_recipe % 10

            state.append(first_recipe)
            state.append(second_recipe)

            yield first_recipe
            yield second_recipe
        else:
            state.append(new_recipe)
            yield new_recipe

        length = len(state)
        first_elf_index = (first_elf_index + state[first_elf_index] + 1) % length
        second_elf_index = (second_elf_index + state[second_elf_index] + 1) % length


def get_score_after(how_long_wait) -> str:
    generator = state_generator()
    [_ for _, r in zip(range(how_long_wait), generator)]
    return ''.join([str(r) for _, r in zip(range(10), generator)])


def test(how_long_wait, excepted: str):
    result = get_score_after(how_long_wait)
    assert result == excepted


test(5, '0124515891')
test(9, '5158916779')
test(18, '9251071085')
test(2018, '5941429882')

print("Solution for first part:", get_score_after(640441))


def find_first_appear(seek: str):
    index = 0
    generator = state_generator()
    actual = deque(maxlen=len(seek))
    compear = deque([int(s) for s in seek])

    while True:
        actual.append(next(generator))
        if actual == compear:
            return index - len(seek) + 1

        index += 1


assert find_first_appear('51589') == 9
assert find_first_appear('01245') == 5
assert find_first_appear('92510') == 18
assert find_first_appear('59414') == 2018

print("Solution for second part:", find_first_appear('640441'))
