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

    with open('new_task_template.py') as in_file:
        with open(os.path.join(str(year), f'{year}_{day_with_zero}.py'), 'w') as out_file:
            out_file.writelines(in_file.read().format(
                day=day,
                year=year,
                day_with_zero=day_with_zero,
                file_input_name=file_input_name
            ))

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
    if input_date.month == 12 and input_date.day <= 25 and not is_solution_for_day_exist(input_date.year, input_date.day):
        return today.year, today.day
    else:
        return find_first_missing(today)


today = date.today()
year, day = for_which_date_create(today)

create_dictionary(year)
create_files(year, day)
open_tabs(year, day)
