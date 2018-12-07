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
