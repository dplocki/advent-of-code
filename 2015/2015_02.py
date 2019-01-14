def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse(lines: [str]):
    for line in lines:
        yield tuple(map(int, line.split('x')))


def calculate_size(l, w, h):
    tmp = l*w, w*h, h*l
    return 2 * sum(tmp) + min(tmp)


def calculate_ribon_length(l, w, h):
    return l * w * h + 2 * min(l + w, w + h, l + h)


# The input is taken: https://adventofcode.com/2015/day/2/input
print("Solution for the first part:", sum([
        calculate_size(l, w, h)
        for l, w, h in parse(load_input_file('input.02.txt'))
    ]))


print("Solution for the second part:", sum([
        calculate_ribon_length(l, w, h)
        for l, w, h in parse(load_input_file('input.02.txt'))
    ]))
