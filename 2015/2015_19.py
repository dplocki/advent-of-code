import re


def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_input(line_generator) -> (dict, []):
    rule_splitter = ' => '
    rules = {}
    molecule = None

    for line in line_generator:
        if len(line) == 0:
            continue
        
        if rule_splitter in line:
            from_what, to_what = line.split(rule_splitter)

            tmp = rules.get(from_what, [])
            tmp.append(to_what)
            rules[from_what] = tmp
        else:
            molecule = line

    return rules, molecule


def solution_for_the_first_part(rules, molecule):
    molecule += '_'  # gaurd
    results = set()

    for from_what, to_what_list in rules.items():
        from_len = len(from_what)

        for to_what in to_what_list:
            index = 0
            while True:
                index = molecule.find(from_what, index + 1)
                if index > -1:
                    results.add(molecule[:index] + to_what + molecule[index + from_len:])
                else:
                    break

    return len(results)


def solution_for_the_second_part(rules, molecule):
    tokens = re.findall(r'([A-Z][a-z]*)', molecule)
    tokens_count = len(tokens)
    brackets = tokens.count('Rn') + tokens.count('Ar')
    comas = tokens.count('Y')

    return tokens_count - brackets - 2 * comas - 1


# The input is taken from: https://adventofcode.com/2015/day/19/input
rules, molecule = parse_input(load_input_file('input.19.txt'))
print("Solution for the first part:", solution_for_the_first_part(rules, molecule))
print("Solution for the second part:", solution_for_the_second_part(rules, molecule))
