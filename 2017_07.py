import re

def find_root_in_file(file_name):
    pattern = re.compile(r'^([a-z]+) \(([0-9]+)\)( -> ([a-z, ]+))?\n$')

    parents = []
    children = []

    with open(file_name) as file:
        for line in file:
            result = pattern.match(line)
            parents.append(result[1])
            if result[4]:
                children.extend(result[4].split(', '))

    for child in children:
        parents.remove(child)

    return parents[0]

print("Main root: ", find_root_in_file('input.txt'))
