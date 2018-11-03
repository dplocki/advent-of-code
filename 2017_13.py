class NonScanner:
    def __init__(self):
        self.index = None

    def move(self):
        pass

class Scanner:
    def __init__(self, layer):
        self.index = 0
        self.layer = layer
        self.direction = 'down'
    
    def move(self):
        if self.direction == 'down':
            self.index += 1
        elif self.direction == 'up':
            self.index -= 1

        if self.index == (self.layer -1):
            self.direction = 'up'
        elif self.index == 0:
            self.direction = 'down'


def test_of_scanner(layer, time_index, expected):
    scanner = Scanner(layer)
    for _ in range(time_index):
        scanner.move()
        
    assert scanner.index == expected, f"Excepted: {expected}, recived: {scanner.index}"

test_of_scanner(3, 0, 0)
test_of_scanner(3, 1, 1)
test_of_scanner(3, 2, 2)
test_of_scanner(3, 3, 1)
test_of_scanner(3, 4, 0)
test_of_scanner(3, 5, 1)
test_of_scanner(3, 6, 2)
test_of_scanner(3, 7, 1)
test_of_scanner(3, 8, 0)

def simulate_walk_on_firewall(input):
    the_lenght_of_input = max(input.keys()) + 1
    firewall = {
        index: Scanner(input[index]) if index in input else NonScanner()
        for index in range(the_lenght_of_input)
    }

    result = 0
    for index in range(the_lenght_of_input):
        current_scaner = firewall[index]
        if current_scaner.index == 0:
            result += current_scaner.layer * index

        # move scanners
        for _, v in firewall.items():
            v.move()

    return result


test_input = {
    0: 3,
    1: 2,
    4: 4,
    6: 4
}

assert simulate_walk_on_firewall(test_input) == 24

input = {
    # get the content of https://adventofcode.com/2017/day/13/input and add the comas on end lines
}

print("Solution for first part: ", simulate_walk_on_firewall(input))
