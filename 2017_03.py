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

def test(cell_number, excepted):
    result = calculate_steps(cell_number)
    assert result == excepted, f"For {cell_number} Excepted: {excepted} Recived: {result}"


test(1, 0)

test(2, 1)
test(3, 2)
test(4, 1)
test(5, 2)

test(12, 3)
test(23, 2)
test(1024, 31)

print(calculate_steps(312051))
