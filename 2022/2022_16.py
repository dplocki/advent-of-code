import collections
import itertools
import re
from typing import Dict, Generator, Iterable, List, Tuple


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[str, int, List[str]], None, None]:
    pattern = re.compile(r'Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)')
    for line in task_input:
        group = pattern.match(line)
        yield group[1], int(group[2]), list(group[3].split(', '))


def calculate_pressure_release(flows: Dict[str, int], solution: Dict[str, int]) -> int:
    return sum((30 - v) * flows[k] for k,v in solution.items())


def shortest_path(leads: Dict[str, List[str]], start: str, end: str) -> int:
    to_check = collections.deque([start])
    cost_so_far = dict()
    cost_so_far[start] = 0

    while to_check:
        point = to_check.pop()

        if point == end:
            return cost_so_far[point]

        for new_point in leads[point]:
            new_cost = cost_so_far[point] + 1

            if new_point not in cost_so_far or new_cost < cost_so_far[new_point]:
                cost_so_far[new_point] = new_cost
                to_check.appendleft(new_point)


def build_cave_map(task_input: Iterable[str]) -> Tuple[Dict[str, Dict[str, int]], Dict[str, int]]:
    tunnel_leads = {}
    flow_rates = {}

    for valve, flow, tunnels in parse(task_input):
        tunnel_leads[valve] = tunnels
        flow_rates[valve] = flow

    cave_map = {
        start:{
            end:shortest_path(tunnel_leads, start, end)
            for end in tunnel_leads.keys()
            if start != end
        }

        for start in tunnel_leads.keys()
    }

    return cave_map, flow_rates


def generate_all_paths(start_time: int, cave_map: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]) -> Generator[Dict[str, int], None, None]:
    possibilities = collections.deque()
    possibilities.append(('AA', start_time, {}))

    non_zero_values = [k for k,v in flow_rates.items() if v > 0]

    while len(possibilities) > 0:
        where, time, valves_state = possibilities.popleft()

        if time >= 30:
            continue

        if flow_rates[where] != 0:
            time += 1 
            valves_state[where] = time
            yield valves_state

        for next_value in non_zero_values:
            if next_value in valves_state:
                continue

            valves_state_copy = valves_state.copy()
            new_time = time + cave_map[where][next_value]
            if new_time < 30:
                possibilities.append((next_value, new_time, valves_state_copy))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    cave_map, flow_rates = build_cave_map(task_input)

    return max(
        calculate_pressure_release(flow_rates, solution)
        for solution in generate_all_paths(0, cave_map, flow_rates))


example_input = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''.splitlines()

#assert solution_for_first_part(example_input) == 1651
# The input is taken from: https://adventofcode.com/2022/day/16/input
task_input = list(load_input_file('input.16.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    cave_map, flow_rates = build_cave_map(task_input)
    non_zero_values = [k for k,v in flow_rates.items() if v > 0]

    solutions = {}

    for valves_state in generate_all_paths(4, cave_map, flow_rates):
        valves_state_hash = 0
        m = 1
        for key in non_zero_values:
            if valves_state.get(key, 0) != 0:
                valves_state_hash += m
            m *= 2

        result_for_valves_state = calculate_pressure_release(flow_rates, valves_state)
        solutions[valves_state_hash] = max(solutions.get(valves_state_hash, 0), result_for_valves_state)

    return max(solutions[n] + solutions[m]
        for n, m in itertools.combinations(solutions, 2)
        if n & m == 0)


assert solution_for_second_part(example_input) == 1707
print("Solution for the second part:", solution_for_second_part(task_input))
