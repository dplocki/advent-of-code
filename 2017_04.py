def checkline_a(line) -> bool:
    passwords = line.split(' ')
    return len(passwords) == len(set(passwords))

assert checkline_a('aa bb cc dd ee') == True
assert checkline_a('aa bb cc dd aa') == False
assert checkline_a('aa bb cc dd aaa') == True

def count_valid_lines_a(file_name) -> int:
    valid_counter = 0
    with open('passwords.txt') as file:
        for line in file:
            if checkline_a(line.rstrip('\n')):
                valid_counter += 1

    return valid_counter

# The content of file is taken from: https://adventofcode.com/2017/day/4/input
print(count_valid_lines_a('passwords.txt'))
