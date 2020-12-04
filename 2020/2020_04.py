def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(task_input: [str]):
    passport = {}
    for line in task_input:

        if line == '':
            yield passport
            passport = {}
            continue
        
        for pair in line.split(' '):
            key, value = pair.split(':')
            passport[key] = value

    yield passport


def solution_for_first_part(passports: [dict]):
    result = 0
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

    for passport in passports:
        if len(required_fields.difference(set(passport.keys()))) == 0:
            result += 1

    return result


assert solution_for_first_part(list(parse('''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''.splitlines()))) == 2


# The input is taken from: https://adventofcode.com/2020/day/4/input
task_input = list(parse(load_input_file('input.04.txt')))
print("Solution for the first part:", solution_for_first_part(task_input))
