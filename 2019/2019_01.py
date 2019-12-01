def load_input_file(file_name):
    with open(file_name) as file:
        yield from (int(line.strip()) for line in file)


def calculate_fuel_mass(x): return x // 3  - 2


# The input is taken from: https://adventofcode.com/2019/day/1/input
all_modules = list(load_input_file('input.01.txt'))

print("Solution for the first part:", sum([calculate_fuel_mass(m) for m in all_modules]))


def calculate_fuel_mass_plus_surplus(x):
    m = calculate_fuel_mass(x)
    if m > 0:
        return m + calculate_fuel_mass_plus_surplus(m)

    return 0


assert calculate_fuel_mass_plus_surplus(1969) == 966
assert calculate_fuel_mass_plus_surplus(100756) == 50346

print("Solution for the second part:", sum([calculate_fuel_mass_plus_surplus(m) for m in all_modules]))
