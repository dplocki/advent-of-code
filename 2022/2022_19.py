from typing import Generator, Iterable
import re


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]):
    pattern = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

    for line in task_input:
        groups = pattern.match(line)
        yield tuple(map(int, (groups[i + 1] for i in range(7))))


def calculate_time_to_purchase(own_amount: int, amount_per_minute: int, needed_amount: int) -> int:
    time = 1
    while own_amount < needed_amount:
        own_amount += amount_per_minute
        time += 1
    
    return time


def find_the_best_geoids(ore_robot_cost_ore: int, clay_robot_cost_ore: int, obsidian_robot_cost_ore: int, obsidian_robot_cost_clay: int, geode_robot_cost_ore: int, geode_robot_cost_obsidian: int) -> int:
    todo = [(0,  0, 0, 0, 0,  1, 0, 0, 0)]
    seen = set()

    while todo:
        time, ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots = todo.pop()
        if time > 24 or (ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots) in seen:
            continue

        seen.add((ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots))

        yield geode + (24 - time) * geode_robots

        # ore robot
        if ore_robots < 5:
            time_to_purchase = calculate_time_to_purchase(ore, ore_robots, ore_robot_cost_ore)
            todo.append((
                time + time_to_purchase,

                ore + ore_robots * time_to_purchase - ore_robot_cost_ore,
                clay + clay_robots * time_to_purchase,
                obsidian + obsidian_robots * time_to_purchase,
                geode + geode_robots * time_to_purchase,
                
                ore_robots + 1, clay_robots, obsidian_robots, geode_robots
            ))

        # clay robot
        if ore_robots < 10:
            time_to_purchase = calculate_time_to_purchase(ore, ore_robots, clay_robot_cost_ore)
            todo.append((
                time + time_to_purchase,

                ore + time_to_purchase * ore_robots - clay_robot_cost_ore,
                clay + time_to_purchase * clay_robots,
                obsidian + obsidian_robots * time_to_purchase,
                geode + geode_robots * time_to_purchase,
                
                ore_robots, clay_robots + 1, obsidian_robots, geode_robots
            ))

        # obsidian robot
        if clay_robots > 0:
            time_to_purchase = max(
                calculate_time_to_purchase(ore, ore_robots, obsidian_robot_cost_ore),
                calculate_time_to_purchase(clay, clay_robots, obsidian_robot_cost_clay))
            todo.append((
                time + time_to_purchase,

                ore + time_to_purchase * ore_robots - obsidian_robot_cost_ore,
                clay + time_to_purchase * clay_robots - obsidian_robot_cost_clay,
                obsidian + obsidian_robots * time_to_purchase,
                geode + geode_robots * time_to_purchase,

                ore_robots, clay_robots, obsidian_robots + 1, geode_robots
            ))

        # geode robot
        if obsidian_robots > 0:
            time_to_purchase = max(
                calculate_time_to_purchase(ore, ore_robots, geode_robot_cost_ore),
                calculate_time_to_purchase(obsidian, obsidian_robots, geode_robot_cost_obsidian))
            todo.append((
                time + time_to_purchase,

                ore + time_to_purchase * ore_robots - geode_robot_cost_ore,
                clay + time_to_purchase * clay_robots,
                obsidian + obsidian_robots * time_to_purchase - geode_robot_cost_obsidian,
                geode + geode_robots * time_to_purchase,

                ore_robots, clay_robots, obsidian_robots, geode_robots + 1
            ))


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        id * max(find_the_best_geoids(ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian))
        for id, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian in parse(task_input))


example_input = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''.splitlines()

assert solution_for_first_part(example_input) == 33
# The input is taken from: https://adventofcode.com/2022/day/19/input
task_input = list(load_input_file('input.19.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
