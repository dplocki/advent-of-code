def steps_generator():
    x = 0
    y = 0
    steps = 0

    yield (x, y)
    while True:
        steps += 1
        
        x += 1
        yield (x, y)
        
        for _ in range(steps):
            y += 1
            yield (x, y)

        steps += 1

        for _ in range(steps):
            x -= 1
            yield (x, y)
        
        for _ in range(steps):
            y -= 1
            yield (x, y)
        
        for _ in range(steps):
            x += 1
            yield (x, y)


def calculate_steps(cell_number):
    generator = steps_generator()
    for _ in range(1, cell_number):
        next(generator)
    
    result = next(generator)

    return abs(result[0]) + abs(result[1])

def test_a(cell_number, excepted):
    result = calculate_steps(cell_number)
    assert result == excepted, f"For {cell_number} Excepted: {excepted} Recived: {result}"


test_a(1, 0)

test_a(2, 1)
test_a(3, 2)
test_a(4, 1)
test_a(5, 2)

test_a(12, 3)
test_a(23, 2)
test_a(1024, 31)


def find_first_written_value_bigger_than(number):
    memory = {(0,0): 1}

    generator = steps_generator()
    next(generator)  # skip one

    while True:
        coordinates = next(generator)
        result = 0

        for x, y in [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == y == 0)]:
            result += memory.get((coordinates[0] + x, coordinates[1] + y), 0)
    
        memory[coordinates] = result

        if result > number:
            return result

# First part
print("Solution of first part: ", calculate_steps(312051))

# Second part
print("Solution of second part: ", find_first_written_value_bigger_than(312051))
