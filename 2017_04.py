def checkline_a(line) -> bool:
    passwords = line.split(' ')
    return len(passwords) == len(set(passwords))

assert checkline_a('aa bb cc dd ee') == True
assert checkline_a('aa bb cc dd aa') == False
assert checkline_a('aa bb cc dd aaa') == True

def count_valid_lines(file_name, checkline) -> int:
    valid_counter = 0
    with open(file_name) as file:
        for line in file:
            if checkline(line.rstrip('\n')):
                valid_counter += 1

    return valid_counter


def checkline_b(line):
    passwords = [''.join(sorted(token)) for token in line.split(' ')]
    return len(passwords) == len(set(passwords))

assert checkline_b('abcde fghij') == True
assert checkline_b('abcde xyz ecdab') == False
assert checkline_b('a ab abc abd abf abj') == True
assert checkline_b('iiii oiii ooii oooi oooo') == True
assert checkline_b('oiii ioii iioi iiio') == False

# The content of file is taken from: https://adventofcode.com/2017/day/4/input
print(count_valid_lines('passwords.txt', checkline_a))
print(count_valid_lines('passwords.txt', checkline_b))
