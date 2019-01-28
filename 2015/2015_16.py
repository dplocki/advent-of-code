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


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def first_parsing_phase(lines: [str]):
    for line in lines:
        yield line.split(': ', 1)


def parse_sue_name(sue_name_with_number):
    return int(sue_name_with_number[len('Sue '):])


def solution_for_first_part(lines: [str]) -> int:
    for sue_name, traits_list in first_parsing_phase(lines):
        traits = traits_list.split(', ')
        if sum(1 for trait in traits if trait in TRAITS_TAPE) == len(traits):
            return parse_sue_name(sue_name)


def solution_for_second_part(lines: [str]):


    def parse_traits(traits: [str]):
        return {
            trait: int(number)
            for trait, number in map(lambda line: line.split(': '), traits)
        }


    def count_matches(traits: dict, pattern_traits: dict):
        result = 0
        
        for trait, count in traits.items():
            pattern_count = pattern_traits[trait]
            if trait in ['cats', 'trees'] and pattern_count < count:
                result += 1
            elif trait in ['pomeranians', 'goldfish'] and pattern_count > count:
                result += 1
            elif pattern_count == count:
                result += 1

        return result


    parsed_original_traits = parse_traits(TRAITS_TAPE.splitlines())

    for sue_name, traits_list in first_parsing_phase(lines):
        traits = parse_traits(traits_list.split(', '))

        if count_matches(traits, parsed_original_traits) == len(traits):
            return parse_sue_name(sue_name)


# The solution is taken from: https://adventofcode.com/2015/day/16/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.16.txt')))
print("Solution for the second part:", solution_for_second_part(load_input_file('input.16.txt')))
