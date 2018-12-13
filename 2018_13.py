def turn_generator():
    while True:
        yield 'l'
        yield 's'
        yield 'r'


class Cart:
    def __init__(self, character):
        self.position = None
        self.character = character
        self.turn = turn_generator()

    def __lt__(self, other_cart):
        if self.position[0] < other_cart.position[0]:
            return True
        elif self.position[0] == other_cart.position[0]:
            return self.position[1] < other_cart.position[1]
        else:
            return False

    def __eq__(self, other_cart):
        return self.position[0] == other_cart.position[0] and self.position[1] == other_cart.position[1]


def parser(input: [str]):
    for y, line in enumerate(input):
        for x, ch in enumerate(line):
            if ch != ' ':
                yield (x, y, ch)


def parse_tokens(parser):
    paths = {}
    carts = []

    for x, y, ch in parser:
        if ch in ['|', '+', '-', '/', '\\']:
            paths[(x, y)] = ch
        else:
            paths[(x, y)] = '-' if ch in ['>', '<'] else '|'
            cart = Cart(ch)
            cart.position = (x, y)
            carts.append(cart)

    return paths, carts


def move_cart(cart, area):
    position = cart.position
    place = area[position]

    if place == '-':
        if cart.character == '>':
            cart.position = (position[0] + 1, position[1])
        elif cart.character == '<':
            cart.position = (position[0] - 1, position[1])
        else:
            raise 'Unknown!'

    elif place == '|':
        if cart.character == '^':
            cart.position = (position[0], position[1] - 1)
        elif cart.character == 'v':
            cart.position = (position[0], position[1] + 1)
        else:
            raise 'Unknown!'

    elif place == '/':
        if cart.character == '>':
            cart.position = (position[0], position[1] - 1)
            cart.character = '^'
        elif cart.character == '<':
            cart.position = (position[0], position[1] + 1)
            cart.character = 'v'
        elif cart.character == '^':
            cart.position = (position[0] + 1, position[1])
            cart.character = '>'
        elif cart.character == 'v':
            cart.position = (position[0] - 1, position[1])
            cart.character = '<'
        else:
            raise 'Unknown!'

    elif place == '\\':
        if cart.character == '>':
            cart.position = (position[0], position[1] + 1)
            cart.character = 'v'
        elif cart.character == '<':
            cart.position = (position[0], position[1] - 1)
            cart.character = '^'
        elif cart.character == '^':
            cart.position = (position[0] - 1, position[1])
            cart.character = '<'
        elif cart.character == 'v':
            cart.position = (position[0] + 1, position[1])
            cart.character = '>'
        else:
            raise 'Unknown!'

    elif place == '+':
        x = next(cart.turn)

        if cart.character == '>':
            if x == 'l':
                cart.position = (position[0], position[1] - 1)
                cart.character = '^'
            elif x == 's':
                cart.position = (position[0] + 1, position[1])
            elif x == 'r':
                cart.position = (position[0], position[1] + 1)
                cart.character = 'v'
            else:
                raise 'Unknown!'

        elif cart.character == '^':
            if x == 'l':
                cart.position = (position[0] - 1, position[1])
                cart.character = '<'
            elif x == 's':
                cart.position = (position[0], position[1] - 1)
            elif x == 'r':
                cart.position = (position[0] + 1, position[1])
                cart.character = '>'
            else:
                raise 'Unknown!'
        
        elif cart.character == '<':
            if x == 'l':
                cart.position = (position[0], position[1] + 1)
                cart.character = 'v'
            elif x == 's':
                cart.position = (position[0] - 1, position[1])
            elif x == 'r':
                cart.position = (position[0], position[1] - 1)
                cart.character = '^'
            else:
                raise 'Unknown!'
        
        elif cart.character == 'v':
            if x == 'l':
                cart.position = (position[0] + 1, position[1])
                cart.character = '>'
            elif x == 's':
                cart.position = (position[0], position[1] + 1)
            elif x == 'r':
                cart.position = (position[0] - 1, position[1])
                cart.character = '<'
            else:
                raise 'Unknown!'

        else:
            raise 'Unknown!'

    else:
        raise 'Unknown!'

    return cart.position


def is_collision(carts):
    return len(set([c.position for c in carts])) != len(carts)


def find_collision(area, carts):
    while True:
        carts.sort()

        for cart in carts:
            cart_position = move_cart(cart, area)

            if is_collision(carts):
                return cart_position


test_1_input = '''/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/       '''.splitlines()
test_2_input = ['''->----<-''']
test_3_input = '''|
v
|
|
|
^
|'''.splitlines()


assert find_collision(*parse_tokens(parser(test_2_input))) == (4, 0)
assert find_collision(*parse_tokens(parser(test_3_input))) == (0, 3)
assert find_collision(*parse_tokens(parser(test_1_input))) == (7, 3)

# Input taken from: https://adventofcode.com/2018/day/13/input
file = open("input.txt", "r")
input_lines = file.read().splitlines()
file.close()

result_position = find_collision(*parse_tokens(parser(input_lines)))
print(f"Solution of first part: {result_position[0]},{result_position[1]} ")


def find_last_cart(area: {}, carts: [Cart]):
    to_removed = []

    while True:
        for r in to_removed:
            carts.remove(r)

        to_removed = []
        if len(carts) == 1:
            return carts[0].position

        carts.sort()
        for cart in carts:
            if cart in to_removed:
                continue

            cart_position = move_cart(cart, area)
            carts_on_position = [cart for cart in carts if cart.position == cart_position]

            if len(carts_on_position) > 1:
                to_removed.extend(carts_on_position)


test_4_input = '''/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/'''.splitlines()

assert find_last_cart(*parse_tokens(parser(test_4_input))) == (6, 4)

result_last_cart_position = find_last_cart(*parse_tokens(parser(input_lines)))
print(f"Solution of second part: {result_last_cart_position[0]},{result_last_cart_position[1]} ")
