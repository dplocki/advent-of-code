import re


def parse_input(input: [str]):
    pattern = re.compile(r'^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$')
    
    for line in input:
        match = pattern.match(line)
        yield match[1], match[2]


test_input = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''.split('\n')


class Node:
    def __init__(self):
        self.needs = []
        self.lead_to = []

    def __repr__(self):
        return  "%r" % (self.__dict__)


def build_graph_table(inputs: [(str, str)]):
    result = {}

    for before_step, after_step,  in inputs:
        after_node = result.get(after_step, Node())
        after_node.needs.append(before_step)

        before_node = result.get(before_step, Node())
        before_node.lead_to.append(after_step)

        result[after_step] = after_node
        result[before_step] = before_node

    return result


test_result_graph_table = build_graph_table(parse_input(test_input))

assert test_result_graph_table['A'].lead_to == ['B', 'D']
assert test_result_graph_table['B'].lead_to == ['E']
assert test_result_graph_table['C'].lead_to == ['A', 'F']
assert test_result_graph_table['D'].lead_to == ['E']
assert test_result_graph_table['E'].lead_to == []
assert test_result_graph_table['F'].lead_to == ['E']

assert test_result_graph_table['A'].needs == ['C']
assert test_result_graph_table['B'].needs == ['A']
assert test_result_graph_table['C'].needs == []
assert test_result_graph_table['D'].needs == ['A']
assert test_result_graph_table['E'].needs == ['B', 'D', 'F']
assert test_result_graph_table['F'].needs == ['C']


def find_all_avaible_steps(graph: {}, steps: str):
    result = set([id for id, node in graph.items() if not node.needs])
    
    for step in steps:
        result.update(graph[step].lead_to)

    for step in steps:
        result.discard(step)

    steps_list = list(steps)
    result = [step for step in result if set(graph[step].needs).issubset(steps_list)]

    return sorted(result)


assert find_all_avaible_steps(test_result_graph_table, '') == ['C']
assert find_all_avaible_steps(test_result_graph_table, 'C') == ['A', 'F']
assert find_all_avaible_steps(test_result_graph_table, 'CA') == ['B', 'D', 'F']
assert find_all_avaible_steps(test_result_graph_table, 'CAB') == ['D', 'F']
assert find_all_avaible_steps(test_result_graph_table, 'CABD') == ['F']
assert find_all_avaible_steps(test_result_graph_table, 'CABDF') == ['E']
assert find_all_avaible_steps(test_result_graph_table, 'CABDFE') == []


def walk_on_the_graph(graph: {}):
    result = ''

    while True:
        pull = find_all_avaible_steps(graph, result)
        if not pull:
            return result

        result += pull[0]


assert walk_on_the_graph(test_result_graph_table) == 'CABDFE'


def load_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


# Taken from https://adventofcode.com/2018/day/7/input
graph = build_graph_table(parse_input(load_file('input.txt')))
print('Solution for the first part:', walk_on_the_graph(graph))


def simple_time_for_step(step: str): return ord(step[0]) - ord('A') + 1
def time_for_step(step: str): return simple_time_for_step(step) + 60


assert time_for_step('A') == 61
assert time_for_step('Z') == 86


def work_concurency_simpulator(graph, workers_number, time_for_step):
    done = ''
    elf_work_on = [None] * workers_number
    seconds = 0
    working_on = []

    while True:
        # Elf working!
        for index in range(workers_number):
            elf_is_working_on = elf_work_on[index]
            if not elf_is_working_on:
                continue

            step, time_left = elf_is_working_on

            time_left -= 1
            if time_left != 0:
                elf_work_on[index] = (step, time_left)
            else:
                elf_work_on[index] = None
                done += step

        # Check what steps are avaible
        avaible_steps = find_all_avaible_steps(graph, done)
        avaible_steps.reverse()
        for work_going_on in working_on:
            if work_going_on in avaible_steps:
                avaible_steps.remove(work_going_on)

        # Elf seeking work
        for index in range(workers_number):
            tmp = elf_work_on[index]
            if not tmp and avaible_steps:
                new_step = avaible_steps.pop()
                elf_work_on[index] = (new_step, time_for_step(new_step))

        # Visualization
        # print(seconds, '|', '  '.join([w[0] if w else '.' for w in elf_work_on]), '|', done)

        # Check who is working...
        working_on = [e[0] for e in elf_work_on if e]
        if not working_on:
            return seconds

        # Tempus fugit
        seconds += 1


assert work_concurency_simpulator(test_result_graph_table, 2, simple_time_for_step) == 15

print('Solution for second part:', work_concurency_simpulator(graph, 4, time_for_step))
