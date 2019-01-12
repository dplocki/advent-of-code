def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_rules(input_lines: [str]) -> {}:
    

    def rotate90(what: str) -> str:
        chars = what.split('/')
        size = len(chars)
        return '/'.join([''.join([chars[y][x] for y in range(size)]) for x in reversed(range(size))])


    def flip(what: str) -> str:
        chars = what.split('/')
        size = len(chars)

        return '/'.join([chars[y][::-1] for y in range(size)])


    def rotate(what: str, value: [str], result):
        tmp = what
        for _ in range(4):
            if tmp not in result:
                result[tmp] = value

            tmp = rotate90(tmp)


    result = {}
    for line in input_lines:
        key, value = line.split(' => ', 1)
        value = value.split('/')

        rotate(key, value, result)
        rotate(flip(key), value, result)

        result[key] = value

    return result


def split_on(size: int, lines: [str], lines_number: int, rules: {str: str}) -> [str]:
    groups_count = lines_number // size
    result = [[None] * groups_count for x in range(groups_count)]

    for x in range(groups_count):
        for y in range(groups_count):
            key = '/'.join([lines[y*size + i][x*size:x*size + size] for i in range(size)])
            result[x][y] = rules[key]

    new_lines = []
    for y in range(groups_count):
        for i in range(size + 1):
            line = ''
            for x in range(groups_count):
                line += result[x][y][i]

            new_lines.append(line)

    return new_lines


def generate_new_state(lines: [str], rules: {str: str}):
    lines_number = len(lines)

    if lines_number % 2 == 0:
        return split_on(2, lines, lines_number, rules)
    elif lines_number % 3 == 0:
        return split_on(3, lines, lines_number, rules)

    return None


def after_n_generations(starting_input: [str], rules: {str: str}, n: int):
    current_state = starting_input
    for _ in range(n):
        current_state = generate_new_state(current_state, rules)

    return current_state


def count_pixes_for_generation(generation: [str]):
    return sum([line.count('#') for line in generation])


STARTING_INPUT = '''.#./..#/###'''.split('/')

testing_input = '''../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#'''.splitlines()

test_rules = parse_rules(testing_input)
test_generation_after_2 = after_n_generations(STARTING_INPUT, test_rules, 2)

assert count_pixes_for_generation(test_generation_after_2) == 12

# The input is taken from: https://adventofcode.com/2017/day/21/input 
task_rules = parse_rules(file_to_input_list('input.21.txt'))
task_generation_after_5 = after_n_generations(STARTING_INPUT, task_rules, 5)

print("The solution for first part: ", count_pixes_for_generation(task_generation_after_5))

task_generation_after_18 = after_n_generations(task_generation_after_5, task_rules, 18 - 5)
print("The solution for second part: ", count_pixes_for_generation(task_generation_after_18))
