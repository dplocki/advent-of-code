from functools import reduce


# code taken from: https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n: int) -> int:
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def number_generator():
    i = 1
    while True:
        yield i
        i += 1


def which_house_first_recieved_presents_number_first_part(how_much_presents: int) -> int:
    just_factors_sum = how_much_presents // 10
    for house_number in number_generator():
        if sum(factors(house_number)) > just_factors_sum:
            return house_number


def which_house_first_recieved_presents_number_second_part(how_much_presents: int) -> int:
    just_factors_sum = how_much_presents // 11
    for house_number in number_generator():
        if sum([f for f in factors(house_number) if f * 50 >= house_number]) > just_factors_sum:
            return house_number


# The input is taken from: https://adventofcode.com/2015/day/20/input
input = 33100000
print("Solution for the first part:", which_house_first_recieved_presents_number_first_part(input))
print("Solution for the second part:", which_house_first_recieved_presents_number_second_part(input))
