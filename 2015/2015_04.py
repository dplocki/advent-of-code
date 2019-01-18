import hashlib


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


def findTheLowestIndex(key):
    check = '0' * 5
    i = 0
    while True:
        if hashlib.md5((key + str(i)).encode()).hexdigest().startswith(check):
            return i

        i += 1


key = load_input_file('input.04.txt')

# The solution is taken from: https://adventofcode.com/2015/day/4/input
print("Solution for the first part:", findTheLowestIndex(key))
