import os
from datetime import date
import webbrowser


def create_dictionary(year: int):
    year_as_string = str(year)
    if not os.path.exists(year_as_string):
        os.mkdir(year_as_string)


def create_files(year: int, day: int):
    day_with_zero = str(day).zfill(2)
    file_input_name = f'input.{day_with_zero}.txt'

    with open(os.path.join(str(year), f'{year}_{day_with_zero}.py'), 'w') as file:
        file.writelines(f'''

def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()

def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)



print(list(
    load_input_file('{file_input_name}')
))


# The input is taken from: https://adventofcode.com/{year}/day/{day}/input

# print("Solution for the first part:", )
''')

    with open(file_input_name, 'w') as file:
        file.writelines('')


def open_tabs(year: int, day: int):
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}/input')
    webbrowser.open(f'https://adventofcode.com/{year}/day/{day}')


def is_solution_for_day_exist(year, day):
    day_with_zero = str(day).zfill(2)
    file_name = f'{year}_{day_with_zero}.py'
    return os.path.exists(os.path.join(str(year), file_name))


def find_first_missing(today):
    for year in range(2015, today.year + 1):
        directory_name = str(year)
        if not os.path.exists(directory_name):
            return year, 1

        for day in range(1, 26):
            if not is_solution_for_day_exist(year, day):
                return year, day


def for_which_date_create(input_date):
    if input_date.month == 12 and not is_solution_for_day_exist(input_date.year, input_date.day):
        return today.year, today.day
    else:
        return find_first_missing(today)


today = date.today()
year, day = for_which_date_create(today)

create_dictionary(year)
create_files(year, day)
open_tabs(year, day)
