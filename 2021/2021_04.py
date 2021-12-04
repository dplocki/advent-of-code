def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


class Board():

    def __init__(self, board) -> None:
        self.board = board
        self.check = set()

    def mark_number(self, number):
        if number in self.board:
            self.check.add(self.board[number])

    def has_line(self):
        for a in range(5):
            if all((a, b) in self.check for b in range(5)) or all((b, a) in self.check for b in range(5)):
                return True

        return False

    def score(self):
        return sum(number for number, position in self.board.items() if position not in self.check)


def parse(task_input: str):

    def parse_board(lines):
        return {int(column) : (row_index, row_column)
            for row_index, row in enumerate(lines.splitlines())
            for row_column, column in enumerate(row.split())}

    groups = list(task_input.split('\n\n'))
    draw_numbers = list(map(int, groups[0].split(',')))
    boards = [Board(parse_board(group)) for group in groups[1:]]

    return draw_numbers, boards


def solution_for_first_part(task_input):
    draw_numbers, boards = parse(task_input)

    for current_number in draw_numbers:
        for board in boards:
            board.mark_number(current_number)
            if board.has_line():
                return current_number * board.score()

    raise Exception('Something goes wrong')


example_input = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

assert solution_for_first_part(example_input) == 4512

# The input is taken from: https://adventofcode.com/2021/day/4/input
task_input = load_input_file('input.04.txt')
print("Solution for the first part:", solution_for_first_part(task_input))
