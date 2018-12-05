# pylint: disable=E1111
import re
import sys


class Computer():

    def __init__(self):
        self.memory = {}
        self.index = 0

    def run_command(self, command, x, p):
        method = getattr(self, command)

        index_offset = method(x, p)
        self.index += 1 if index_offset is None else index_offset

    def set(self, x, p):
        self.memory[x] = self._register_or_number(p)

    def add(self, x, p):
        self.memory[x] = self.memory.get(x, 0) + self._register_or_number(p)

    def mul(self, x, p):
        self.memory[x] = self.memory.get(x, 0) * self._register_or_number(p)

    def mod(self, x, p):
        self.memory[x] = self.memory.get(x, 0) % self._register_or_number(p)

    def jgz(self, x, p):
        if self._register_or_number(x) > 0:
            return self._register_or_number(p)

    def _register_or_number(self, p) -> int:
        if p.isalpha():
            return self.memory.get(p, 0)
        else:
            return int(p)


class FirstPartComputer(Computer):

    def __init__(self):
        Computer.__init__(self)
        self.last_play_frequency = None

    def rcv(self, x, p):
        if self.memory.get(x, 0) > 0:
            print("Solution for first part:", self.last_play_frequency)
            return sys.maxsize

    def snd(self, x, p):
        self.last_play_frequency = self.memory.get(x, 0)


    def run_program(self, program: []):
        program_len = len(program)

        while self.index < program_len:
            command = program[self.index]

            self.run_command(*command)


class SecondPartComputer(Computer):

    def __init__(self, program_id):
        Computer.__init__(self)
        self.to_send = []
        self.recived = None
        self.count_send = 0
        self.program_id = program_id
        self.memory['p'] = program_id
        self.last_command = None

    def rcv(self, x, p):
        self.memory[x] = self.recived

    def snd(self, x, p):
        self.count_send += 1
        self.to_send.insert(0, self._register_or_number(x))

    def run_program(self, program: []):
        program_len = len(program)

        while self.index < program_len:
            command = program[self.index]
            #print(f'[{self.program_id}] {self.index} ', *command)
            self.last_command = command[0]

            if self.last_command == 'rcv':
                yield self.last_command

            self.run_command(*command)

            if self.last_command == 'snd':
                yield self.last_command


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
    computer_0 = SecondPartComputer(0)
    computer_0.generator = computer_0.run_program(commands)

    computer_1 = SecondPartComputer(1)
    computer_1.generator = computer_1.run_program(commands)

    active = computer_0
    non_active = computer_1

    while computer_0.last_command != 'rcv' or computer_1.last_command != 'rcv':
        tmp = next(active.generator)

        if tmp == 'rcv':
            if non_active.to_send:
                active.recived = non_active.to_send.pop()
                continue

        elif tmp != 'snd':
            continue

        active, non_active = non_active, active

    return {
        computer_0.program_id: computer_0.count_send,
        computer_1.program_id: computer_1.count_send
    }


# # Solution for the first part
commands = [_ for _ in parse_lines(load_file('input.18.txt'))]
# computer = FirstPartComputer()
# computer.run_program(commands)

# Tests for second part
test_commands = [_ for _ in parse_lines(['snd 1', 'snd 2', 'snd p', 'rcv a', 'rcv b', 'rcv c', 'rcv d'])]

test_computer = SecondPartComputer(0)
for a, b in zip(test_computer.run_program(test_commands), ['snd'] * 3 + ['rcv'] * 4):
    assert a == b, f"Excepted {b}, recived {a}"

assert test_computer.to_send == [0, 2, 1]

test_computer = SecondPartComputer(1)
for a, b in zip(test_computer.run_program(test_commands), ['snd'] * 3 + ['rcv'] * 4):
    assert a == b, f"Excepted {b}, recived {a}"

assert test_computer.to_send == [1, 2, 1]
assert run_parallel_programs(test_commands) == {0: 3, 1: 3}

test_commands_2 = [_ for _ in parse_lines(['snd 1', 'rcv a', 'snd 2', 'rcv b', 'snd p', 'rcv c', 'rcv d'])]

print(run_parallel_programs(commands))
