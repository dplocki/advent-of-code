# pylint: disable=E1111
import re
import sys
from collections import deque


class Computer():

    def __init__(self):
        self._memory = {}
        self._index = 0

    def run_command(self, command, x, p):
        method = getattr(self, command)

        index_offset = method(x, p)
        self._index += (index_offset if index_offset is not None else 1)

    def set(self, x, p):
        self._memory[x] = self._register_or_number(p)

    def add(self, x, p):
        self._memory[x] = self._register_or_number(x) + self._register_or_number(p)

    def mul(self, x, p):
        self._memory[x] = self._register_or_number(x) * self._register_or_number(p)

    def mod(self, x, p):
        self._memory[x] = self._register_or_number(x) % self._register_or_number(p)

    def jgz(self, x, p):
        if self._register_or_number(x) > 0:
            return self._register_or_number(p)

    def _register_or_number(self, p) -> int:
        return self._memory.get(p, 0) if p.isalpha() else int(p)


class FirstPartComputer(Computer):

    def __init__(self):
        Computer.__init__(self)
        self.last_play_frequency = None

    def rcv(self, x, p):
        if self._memory.get(x, 0) > 0:
            print("Solution for first part:", self.last_play_frequency)
            return sys.maxsize

    def snd(self, x, p):
        self.last_play_frequency = self._memory.get(x, 0)

    def run_program(self, program: []):
        program_len = len(program)

        while self._index < program_len:
            command = program[self._index]

            self.run_command(*command)


class SecondPartComputer(Computer):

    def __init__(self, program_id, program):
        Computer.__init__(self)

        self.recived = deque()
        self.count_send = 0
        self.program_id = program_id
        self._memory['p'] = program_id
        self.other_computer = None
        self.program = program
        self.program_length = len(program)
        self.terminated = False
        self.blocked = False

    def run_program(self):
        self.terminated = self._index < 0 or self._index >= self.program_length
        if self.terminated:
            return

        command, first_paramater, second_paramater = self.program[self._index]
        if command == 'rcv':
            if self.recived:
                self._memory[first_paramater] = self.recived.popleft()
                self._index += 1
            else:
                self.blocked = True
                return
        elif command == 'snd':
            self.count_send += 1
            self.other_computer.recived.append(self._register_or_number(first_paramater))
            self.other_computer.blocked = False
            self._index += 1
        else:
            self.run_command(command, first_paramater, second_paramater)

    def is_working(self):
        return not self.terminated and not self.blocked        

def load_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_lines(inputs: []):
    pattern = re.compile(r'^([a-z]{3}) ([0-9a-z])( ([\-0-9a-z]+))?')
    for line in inputs:
        group = pattern.match(line)
        yield (group[1], group[2], group[4])


def run_parallel_programs(commands):
    computer_0 = SecondPartComputer(0, commands)
    computer_1 = SecondPartComputer(1, commands)

    computer_0.other_computer = computer_1
    computer_1.other_computer = computer_0

    while computer_0.is_working() or computer_1.is_working():
        computer_1.run_program()
        computer_0.run_program()

    return {
        computer_0.program_id: computer_0.count_send,
        computer_1.program_id: computer_1.count_send
    }

# Solution for the first part, the input take from https://adventofcode.com/2017/day/18/input
commands = [_ for _ in parse_lines(load_file('input.18.txt'))]
computer = FirstPartComputer()
computer.run_program(commands)

result = run_parallel_programs(commands)
print('Solution for second part:', result[1])
