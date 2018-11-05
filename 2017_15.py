def generator(factor, prev):
    while True:
        yield prev
        
        # 2147483647 is prime
        prev = (prev * factor) % 2147483647


def generatorA(prev):
    # 16807 -> (7, 7, 7, 7, 7)
    return generator(16807, prev)


def generatorB(prev):
    # 48271 is prime
    return generator(48271, prev)


def jugde_generator(how_much, prev_for_a, prev_for_b):
    _16bit = 2**16

    result = 0
    for a, b, _ in zip(generatorA(prev_for_a), generatorB(prev_for_b), range(how_much)):
        if a % _16bit == b % _16bit:
            result += 1

    return result


assert jugde_generator(5, 65, 8921) == 1
assert jugde_generator(40000000, 65, 8921) == 588

print("Solution for first part:", jugde_generator(40000000, 289, 629))
