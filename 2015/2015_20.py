from functools import reduce


# code taken from: https://stackoverflow.com/questions/6800193/what-is-the-most-efficient-way-of-finding-all-the-factors-of-a-number-in-python
def factors(n: int) -> int:
    return set(reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))


def which_house_first_recieved_presents_number(how_much_presents: int ) -> int:


    def infity_generator():
        i = 1
        while True:
            yield i
            i += 1


    just_sum_factors = how_much_presents // 10
    for house_number in infity_generator():
        if sum(factors(house_number)) > just_sum_factors:
            return house_number


# The input is taken from: https://adventofcode.com/2015/day/20/input
print("Solution for the first part:", which_house_first_recieved_presents_number(33100000))
