import string


class Node:

    def __init__(self, value, next):
        self.next = next
        self.prev = None
        self.value = value

    def __repr__(self):
        return f'[{self.value}]'


class List:

    def __init__(self, base_string):
        self.length = len(base_string)

        self.dictionary = {}
        nextTmp = None
        for letter in base_string[::-1]:
            tmp = Node(letter, nextTmp)
            if nextTmp:
                nextTmp.prev = tmp

            self.dictionary[letter] = tmp
            nextTmp = tmp

        self.dictionary['^'] = self.dictionary[base_string[0]]
        self.dictionary['$'] = self.dictionary[base_string[-1:]]

    def _nodes_from_begining(self):
        node = self.dictionary['^']

        while node != None:
            yield node
            node = node.next

    def _nodes_from_end(self):
        node = self.dictionary['$']

        while node != None:
            yield node
            node = node.prev

    def to_string(self):
        return ''.join([v.value for v in self._nodes_from_begining()])

    def find_node(self, index: int):
        if index == 0:
            return self.dictionary['^']

        node = self.dictionary['^']
        for _ in range(index):
            node = node.next

        return node

    def spin(self, how_many: int):
        node = self.dictionary['$']
        for _ in range(how_many - 1):
            node = node.prev

        self.dictionary['^'].prev = self.dictionary['$']
        self.dictionary['$'].next = self.dictionary['^']
        
        self.dictionary['^'] = node
        self.dictionary['$'] = node.prev

        self.dictionary['^'].prev = None
        self.dictionary['$'].next = None

    def partner(self, letter_1, letter_2):
        node_1 = self.dictionary[letter_1]
        node_2 = self.dictionary[letter_2]

        self._swap(node_1, node_2)

    def exchange(self, index_1: int, index_2: int):
        node_1 = self.find_node(index_1)
        node_2 = self.find_node(index_2)

        self._swap(node_1, node_2)

    def _swap(self, node_1, node_2):
        self.dictionary[node_1.value] = node_2
        self.dictionary[node_2.value] = node_1
        
        node_1.value, node_2.value = node_2.value, node_1.value


def check_integration_of_node_dictionary(node_dictionary: List, excepted_string):
    for letter in node_dictionary.dictionary:
        assert letter in node_dictionary.dictionary, "Missing letter from base string"

    expected_first_letter = excepted_string[0]
    received_first_letter = node_dictionary.dictionary['^'].value
    assert received_first_letter == expected_first_letter, f"Excepted that first letter will be '{expected_first_letter}' recived: '{received_first_letter}'"

    expected_last_letter = excepted_string[-1:]
    received_last_letter = node_dictionary.dictionary['$'].value
    assert received_last_letter == expected_last_letter, f"Excepted that first letter will be '{expected_last_letter}' recived: '{received_last_letter}'"

    result = node_dictionary.to_string()
    assert result == excepted_string, f'Recived: "{result}", excepted: "{excepted_string}"'

    for node, letter in zip(node_dictionary._nodes_from_begining(), excepted_string):
        assert node.value == letter, f"Excepted {letter}, recived {node.value}"

    for node, letter in zip(node_dictionary._nodes_from_end(), excepted_string[::-1]):
        assert node.value == letter, f"Excepted {letter}, recived {node.value}"


def test_of_node_dictionary(base_string):
    base_list = List(base_string)
    
    check_integration_of_node_dictionary(base_list, base_string)

test_of_node_dictionary('a')
test_of_node_dictionary('abc')
test_of_node_dictionary('abcdefg')


def test_of_find_node(base_string: str, index: int, excepted: str):
    test_list = List(base_string)
    node = test_list.find_node(index)

    assert node.value == excepted, f"Excepted: {excepted}, recived: {node.value}"


test_of_find_node('abcdef', 0, 'a')
test_of_find_node('abcdef', 3, 'd')
test_of_find_node('abcdef', 5, 'f')


def test_of_spin(base_string: str, from_index: int, excepted_string: str):
    base_list = List(base_string)
    base_list.spin(from_index)

    check_integration_of_node_dictionary(base_list, excepted_string)


test_of_spin('abcde', 1, 'eabcd')
test_of_spin('abcde', 3, 'cdeab')
test_of_spin('abcde', 5, 'abcde')


def test_of_partner(base_string: str, letter_1: str, letter_2: str, excepted_string: str):
    base_list = List(base_string)
    base_list.partner(letter_1, letter_2)

    check_integration_of_node_dictionary(base_list, excepted_string)


test_of_partner('abcdef', 'b', 'd', 'adcbef')
test_of_partner('abcde', 'a', 'c', 'cbade')
test_of_partner('abcde', 'c', 'e', 'abedc')
test_of_partner('abcde', 'a', 'e', 'ebcda')
test_of_partner('eabdc', 'e', 'b', 'baedc')


def test_of_exchange(base_string: str, index_1: int, index_2: int, excepted_string: str):
    base_list = List(base_string)
    base_list.exchange(index_1, index_2)

    check_integration_of_node_dictionary(base_list, excepted_string)


test_of_exchange('abcdef', 1, 3, 'adcbef')
test_of_exchange('abcdef', 0, 1, 'bacdef')
test_of_exchange('abcdef', 0, 5, 'fbcdea')


def run_instruction(list: List, instruction):
    if instruction[0] == 's':
        list.spin(int(instruction[1:]))
    elif instruction[0] == 'x':
        list.exchange(*[int(t) for t in instruction[1:].split('/')])
    elif instruction[0] == 'p':
        list.partner(*(instruction[1:].split('/')))


def test_of_instruction(base_string, instruction, excepted_string):
    base_list = List(base_string)
    run_instruction(base_list, instruction)

    check_integration_of_node_dictionary(base_list, excepted_string)


test_of_instruction('abcde', 's1', 'eabcd')
test_of_instruction('eabcd', 'x3/4', 'eabdc')
test_of_instruction('eabdc', 'pe/b', 'baedc')


import string

list = List(string.ascii_lowercase[:16])
with open('input.txt') as file:
    for line in file:
        run_instruction(list, line[:-1])

print('Solution for first part:', list.to_string())
