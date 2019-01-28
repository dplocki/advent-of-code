def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def solution_for_first_part(lines: [str]) -> int:
    TRAITS_TAPE = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

    for line in lines:
        sue_name, traits_list = line.split(': ', 1)

        traits = traits_list.split(', ')
        if sum(1 for trait in traits if trait in TRAITS_TAPE) == len(traits):
            return int(sue_name[len('Sue '):])


# The solution is taken from: https://adventofcode.com/2015/day/16/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.16.txt')))
