def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def hash(value: str) -> int:
    result = 0

    for character in value:
        result += ord(character)
        result *= 17
        result %= 256

    return result


def solution_for_first_part(task_input: str) -> int:
    return sum(map(hash, task_input.split(',')))


example_input = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

assert solution_for_first_part(example_input) == 1320

# The input is taken from: https://adventofcode.com/2023/day/15/input
task_input = load_input_file('input.15.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:
    boxes = {box_index:[] for box_index in range(256)}

    for instruction in task_input.split(','):
        tokens = instruction.replace('-', ' ').replace('=', ' ').split(' ')
        label = tokens[0]
        number =  int(tokens[1]) if not '-' in instruction else None
        box = boxes[hash(label)]
        labels = [label for label, _ in box]

        if '-' in instruction:
            if label in labels:
                box.pop(labels.index(label))
        elif '=' in instruction:
            if label in labels:
                box[labels.index(label)] = (label, number)
            else:
                box.append((label, number))

    return sum(
        (key + 1) * (i + 1) * b[1]
        for key, box in boxes.items()
        for i, b in enumerate(box))


assert solution_for_second_part(example_input) == 145
print("Solution for the second part:", solution_for_second_part(task_input))
