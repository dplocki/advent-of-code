def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse_input(line_generator) -> (dict, []):
    rule_splitter = ' => '
    rules = {}
    molecule = None

    for line in line_generator:
        if len(line) > 0:
            if rule_splitter in line:
                from_what, to_what = line.split(rule_splitter)

                tmp = rules.get(from_what, [])
                tmp.append(to_what)
                rules[from_what] = tmp
            else:
                molecule = line

    return rules, molecule


def all_possible_molecule_after_change(rules, molecule):
    molecule += '_'
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

    return results


# The solution is taken from: https://adventofcode.com/2015/day/19/input
print("Solution for the first part:", len(all_possible_molecule_after_change(*parse_input(load_input_file('input.19.txt')))))
