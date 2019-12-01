def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)

def calculate_fuel_mass(x): return x // 3  - 2

# The input is taken from: https://adventofcode.com/2019/day/1/input
all_modules = list(load_input_file('input.01.txt'))

print("Solution for the first part:", sum([calculate_fuel_mass(m) for m in all_modules]))

