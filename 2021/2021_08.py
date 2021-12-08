from typing import Tuple


def load_input_file(file_name: str) -> list[str]:
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: list[str]) -> Tuple[list[set], list[set]]:
    for line in task_input:
        tokens = line.split(' | ')
        yield list(map(set, tokens[0].split())), list(map(set, tokens[1].split()))


def only_with_size(size: int) -> bool:
    return lambda pattern: len(pattern) == size


def patterns_to_size_dictionary(patterns: list[set]) -> dict[int, list[set]]:
    return {size:list(filter(only_with_size(size), patterns)) for size in range(2, 8)}


def solution_for_first_part(task_input: Tuple[list[set], list[set]]) -> int:
    result = 0
    for patterns, outputs in parse(task_input):
        patterns_pre_size = patterns_to_size_dictionary(patterns)

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


MULTIPLAYERS = (1000, 100, 10, 1)


def solution_for_second_part(task_input: Tuple[list[set], list[set]]) -> int:
    result = 0
    for patterns, outputs in parse(task_input):
        patterns_pre_size = patterns_to_size_dictionary(patterns)

        digits = {}
        digits[1] = patterns_pre_size[2][0]
        digits[4] = patterns_pre_size[4][0]
        digits[7] = patterns_pre_size[3][0]
        digits[8] = patterns_pre_size[7][0]

        digits[9] = next(filter(lambda p: digits[4].issubset(p), patterns_pre_size[6]))
        patterns_pre_size[6].remove(digits[9])

        digits[3] = next(filter(lambda p: digits[7].issubset(p), patterns_pre_size[5]))
        patterns_pre_size[5].remove(digits[3])

        zero_excluder = digits[4] - digits[1]
        digits[0] = next(filter(lambda p: not zero_excluder.issubset(p), patterns_pre_size[6]))
        patterns_pre_size[6].remove(digits[0])

        digits[6] = patterns_pre_size[6][0]

        five_excluder = list(digits[8] - digits[9])[0]
        digits[2] = next(filter(lambda p: five_excluder in p, patterns_pre_size[5]))
        patterns_pre_size[5].remove(digits[2])
        digits[5] = patterns_pre_size[5][0]

        result += sum(digit * multiplayer
            for digit, multiplayer in zip(
                    (next(digit for digit, combination in digits.items() if output == combination) for output in outputs),
                    MULTIPLAYERS))
    
    return result


assert solution_for_second_part(example_input) == 61229

print("Solution for the second part:", solution_for_second_part(task_input))
