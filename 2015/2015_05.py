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


def is_nice_first_part(line: str) -> bool:
    return has_at_least_three_vowels(line) and has_double_letters(line) and not contain_forbiden(line)


assert is_nice_first_part('ugknbfddgicrmopn') == True
assert is_nice_first_part('aaa') == True
assert is_nice_first_part('jchzalrnumimnmhp') == False
assert is_nice_first_part('haegwjzuvuyypxyu') == False
assert is_nice_first_part('dvszwmarrgswjxmb') == False


# The solution is taken from: https://adventofcode.com/2015/day/5/input
print("Solution for the first part:", sum(1 for line in load_input_file('input.05.txt') if is_nice_first_part(line)))


def has_twice_pair_not_overlapping(line: str) -> bool:
    f, s = itertools.tee(line)
    next(s)

    for i, t in enumerate(zip(f, s)):
        if line.find(t[0] + t[1], i + 2) > -1:
            return True

    return False


def same_letter_with_one_between(line: str) -> bool:
    f, s = itertools.tee(line)
    next(s)
    next(s)
    
    for a, b in zip(f, s):
        if a == b:
            return True

    return False


def is_nice_second_part(line: str) -> bool:
    return has_twice_pair_not_overlapping(line) and same_letter_with_one_between(line)


assert is_nice_second_part('qjhvhtzxzqqjkmpb') == True
assert is_nice_second_part('xxyxx') == True
assert is_nice_second_part('uurcxstgmygtbstg') == False
assert is_nice_second_part('ieodomkazucvgmuy') == False

# The input taken from: https://adventofcode.com/2015/day/5/input
print("Solution for the second part:", sum(1 for line in load_input_file('input.05.txt') if is_nice_second_part(line)))
