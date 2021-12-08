def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]):
    for line in task_input:
        tokens = line.split(' | ')
        yield list(map(set, tokens[0].split())), list(map(set, tokens[1].split()))


def solution_for_first_part(task_input):

    def only_with_size(size):
        return lambda pattern: len(pattern) == size

    lines = list(parse(task_input))
    
    result = 0
    for patterns, outputs in lines:
        patterns_pre_size = {size:list(filter(only_with_size(size), patterns)) for size in range(2, 8)}

        result += sum(1
            for output in outputs
            for i in (2, 3, 4, 7) if patterns_pre_size[i][0] == output)

    return result


example_input = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''.splitlines()

assert solution_for_first_part(example_input) == 26

# The input is taken from: https://adventofcode.com/2021/day/8/input
task_input = list(load_input_file('input.08.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
