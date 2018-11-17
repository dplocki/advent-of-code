# pylint: disable=E1111
import re
import sys


class Computer():

    def __init__(self):
        self.last_play_frequency = None
        self.memory = {}
        self.index = 0

    def run_command(self, command, x, p):
        method = getattr(self, command)
        return method(x, p)

    def run_program(self, program):
        program_len = len(commands)

        while self.index < program_len:
            command = program[self.index]
            index_offset = self.run_command(*command)
            if index_offset is None:
                self.index += 1
            else:
                self.index += index_offset

    def snd(self, x, p):
        self.last_play_frequency = self.memory.get(x, 0)

    def set(self, x, p):
        self.memory[x] = self._register_or_number(p)

    def add(self, x, p):
        self.memory[x] = self.memory.get(x, 0) + self._register_or_number(p)

    def mul(self, x, p):
        self.memory[x] = self.memory.get(x, 0) * self._register_or_number(p)

    def mod(self, x, p):
        self.memory[x] = self.memory.get(x, 0) % self._register_or_number(p)

    def rcv(self, x, p):
        if self.memory.get(x, 0) > 0:
            print("Playing:", self.last_play_frequency)
            return sys.maxsize

    def jgz(self, x, p):
        if self._register_or_number(x) > 0:
            return int(p)

    def _register_or_number(self, p) -> int:
        if p in self.memory:
            return self.memory[p]
        else:
            return int(p)


def load_instruction(file_name: str):
    pattern = re.compile(r'^([a-z]{3}) ([0-9a-z])( ([\-0-9a-z]+))?\n')

    with open(file_name) as file:
        for line in file:
            group = pattern.match(line)
            yield (group[1], group[2], group[4])


commands = [_ for _ in load_instruction('input.18.txt')]
computer = Computer()
computer.run_program(commands)
