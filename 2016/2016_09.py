def load_input_file(file_name):
    with open(file_name) as file:
        return file.read()


class Parser():

    def __init__(self):
        self.state = self.normal
        self.buffor = ''
        self.how_many_letters = 0
        self.how_many_repeat = 0

    def normal(self, char):
        if char == '(':
            self.state = self.marker
            return

        return char

    def marker(self, char):
        if char == ')':
            self.how_many_letters, self.how_many_repeat = map(int, self.buffor.split('x'))
            self.state = self.repeat
            self.buffor = ''
        else:
            self.buffor += char

    def repeat(self, char):
        self.buffor += char
        self.how_many_letters -= 1

        if self.how_many_letters == 0:
            tmp = self.buffor * self.how_many_repeat
            self.buffor = ''
            self.state = self.normal

            return tmp

    def decompression(self, line):
        for char in line:
            if char.isspace():
                continue

            result = self.state(char)
            if result != None:
                yield from result


def decompressed_length(line: str):
    return sum([1 for _ in Parser().decompression(line)])


assert decompressed_length('ADVENT') == 6
assert decompressed_length('A(1x5)BC') == 7
assert decompressed_length('(3x3)XYZ') == 9
assert decompressed_length('A(2x2)BCD(2x2)EFG') == 11
assert decompressed_length('(6x1)(1x3)A') == 6
assert decompressed_length('X(8x2)(3x3)ABCY') == 18

# The input is taken from: https://adventofcode.com/2016/day/9/input
input_string = load_input_file('input.09.txt')
print("Solution for the first part:", decompressed_length(input_string))
