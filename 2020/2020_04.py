import re


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


def check_require_fields(passports: [dict]) -> [dict]:
    result = 0
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

    for passport in passports:
        if len(required_fields.difference(set(passport.keys()))) == 0:
            yield passport


def solution_for_first_part(passports: [dict]) -> int:
    return sum(1 for _ in check_require_fields(passports))


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


def validate_passports(passports: [dict]) -> [dict]:

    def is_in_range_check(_from, _to, key):
        return lambda passport: _from <= int(passport[key]) <= _to 


    def check_height(passport: dict) -> bool:
        value = passport['hgt']
        if not('cm' in value or 'in' in value):
            return False

        unit = value[-2:]
        height = int(value[:-2])

        if unit == 'cm':
            return 150 <= height <= 193

        elif unit == 'in':
            return 59 <= height <= 76

        return False


    def pattern_check(pattern, key):
        checker = re.compile(f'^{pattern}$')
        return lambda passport: checker.match(passport[key])


    def check_eye_colour(passport: dict) -> bool:
        return passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


    def check_by_validators(validators, passport):
        for validator in validators:
            if not validator(passport):
                return False

        return True


    validators = {
        is_in_range_check(1920, 2002, 'byr'),
        is_in_range_check(2010, 2020, 'iyr'),
        is_in_range_check(2020, 2030, 'eyr'),
        check_height,
        pattern_check('#[0-9a-f]{6}', 'hcl'),
        check_eye_colour,
        pattern_check('\d{9}', 'pid')
    }

    yield from (passport for passport in passports if check_by_validators(validators, passport))



def solution_for_second_part(passports: [dict]) -> int:
    return sum(1 for _ in validate_passports(check_require_fields(passports)))


assert solution_for_second_part(parse('''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''.splitlines())) == 0

assert solution_for_second_part(parse('''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''.splitlines())) == 4

print("Solution for the second part:", solution_for_second_part(task_input))
