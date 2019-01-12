import re


def parser(file_name):
    pattern = re.compile(r'^(\d+) <-> ([0-9, ]+)\n$')

    with open(file_name) as file:
        for line in file:
            group = pattern.match(line)
            yield int(group[1]), [int(_) for _ in group[2].split(', ')]


def find_all_in_group(dictionary: {}, node: int, already_acounted: set = set()) -> set:
    direct_contact = dictionary[node]
    result = set(direct_contact)
    result.add(node)

    for neighbor in direct_contact:
        if neighbor in already_acounted:
            continue

        result |= find_all_in_group(dictionary, neighbor, result)

    return result


dictionary = {root: children for root, children in parser('input.txt')}
print("Solution for first part:", len(find_all_in_group(dictionary, 0)))

groups = 0
checked = []
for k, _ in dictionary.items():
    if k not in checked:
        checked += find_all_in_group(dictionary, k)
        groups += 1

print("Solution for second part:", groups)
