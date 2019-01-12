def generator(factor, prev):
    while True:
        yield prev
        
        # 2147483647 is prime
        prev = (prev * factor) % 2147483647


def picky_generator(generator, multiple):
    for g in generator:
        if g % multiple == 0:
            yield g


def generatorA(prev):
    # 16807 -> (7, 7, 7, 7, 7)
    return generator(16807, prev)


def generatorB(prev):
    # 48271 is prime
    return generator(48271, prev)


def jugde_generator(how_much, generator_a, generator_b):
    _16bit = 2**16

    result = 0
    for a, b, _ in zip(generator_a, generator_b, range(how_much)):
        if a % _16bit == b % _16bit:
            result += 1

    return result


def jugde_generator_1(how_much, prev_for_a, prev_for_b):
    return jugde_generator(how_much, generatorA(prev_for_a), generatorB(prev_for_b))


def jugde_generator_2(how_much, prev_for_a, prev_for_b):
    return jugde_generator(how_much,
                           picky_generator(generatorA(prev_for_a), 4),
                           picky_generator(generatorB(prev_for_b), 8))


assert jugde_generator_1(5, 65, 8921) == 1
assert jugde_generator_1(4 * 10 ** 7, 65, 8921) == 588

print("Solution for first part:", jugde_generator_1(4 * 10 ** 7, 289, 629))

assert jugde_generator_2(5, 65, 8921) == 0
assert jugde_generator_2(1056, 65, 8921) == 1
assert jugde_generator_2(5 * 10 ** 6, 65, 8921) == 309

print("Solution for second part:", jugde_generator_2(5 * 10 ** 6, 289, 629))
