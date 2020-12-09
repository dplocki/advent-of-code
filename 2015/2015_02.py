def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines: [str]):
    yield from (
            tuple(map(int, line.split('x')))
            for line in lines
        )


def calculate_size(l, w, h):
    tmp = l*w, w*h, h*l
    return 2 * sum(tmp) + min(tmp)


def calculate_ribon_length(l, w, h):
    return l * w * h + 2 * min(l + w, w + h, l + h)


# The input is taken: https://adventofcode.com/2015/day/2/input
task_input = list(parse(load_input_file('input.02.txt')))
print("Solution for the first part:", sum(calculate_size(l, w, h) for l, w, h in task_input))
print("Solution for the second part:", sum(calculate_ribon_length(l, w, h) for l, w, h in task_input))
