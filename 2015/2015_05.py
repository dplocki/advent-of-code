import itertools


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def has_at_least_three_vowels(line: str) -> bool:
    return sum(line.count(letter) for letter in 'aeiou') >= 3


def has_double_letters(line: str) -> bool:
    f, s = itertools.tee(line)
    next(f, None)
    
    for a, b in zip(f, s):
        if a == b:
            return True

    return False


def contain_forbiden(line: str) -> bool:
    return 'ab' in line or 'cd' in line or 'pq' in line or 'xy' in line


def is_nice(line: str) -> bool:
    return has_at_least_three_vowels(line) and has_double_letters(line) and not contain_forbiden(line)


assert is_nice('ugknbfddgicrmopn') == True
assert is_nice('aaa') == True
assert is_nice('jchzalrnumimnmhp') == False
assert is_nice('haegwjzuvuyypxyu') == False
assert is_nice('dvszwmarrgswjxmb') == False


# The solution is taken from: https://adventofcode.com/2015/day/5/input
print("Solution for the first part:", sum(1 for line in load_input_file('input.05.txt') if is_nice(line)))
