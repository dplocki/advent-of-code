def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse(lines: [str]):
    for line in lines:
        yield tuple(map(int, line.split('x')))


def calculate_size(l, w, h):
    return  2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, l*h)


# The input is taken: https://adventofcode.com/2015/day/2/input
print("Solution for the first part:", sum([
        calculate_size(l, w, h)
        for l, w, h in parse(load_input_file('input.02.txt'))
    ]))
