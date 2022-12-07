from typing import Dict, Generator, List


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def build_data_structure(task_input: List[str]) -> Dict[str, int]:
    ROOT = '#'
    data_structure = { ROOT: 0 }
    current_directory = [ ROOT ]

    for line in task_input:
        tokens = line.split(' ')

        if tokens[0] == '$' and tokens[1] == 'cd':
            if tokens[2] == '/':
                current_directory = [ ROOT ]
            elif tokens[2] == '..':
                current_directory.pop()
            else:
                current_directory.append(tokens[2])
        elif tokens[0] == '$' and tokens[1] == 'ls':
            pass
        elif tokens[0] == 'dir':
            data_structure['/'.join(current_directory) + '/' + tokens[1]] = 0
        else:
            size = int(tokens[0])

            tmp_directory = ROOT
            for dir in current_directory[1:]:
                tmp_directory += '/' + dir
                data_structure[tmp_directory] += size

    return data_structure


def solution_for_first_part(task_input) -> int:
    data_structure = build_data_structure(task_input)

    return sum(v for v in data_structure.values() if v < 100_000)


example_input = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''.splitlines()

assert solution_for_first_part(example_input) == 95437
# The input is taken from: https://adventofcode.com/2022/day/7/input
task_input = list(load_input_file('input.07.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
