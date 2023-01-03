from typing import Generator, Iterable, Tuple
from functools import reduce
from operator import mul
import re


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def parse(task_input: Iterable[str]) -> Generator[Tuple[int, ...], None, None]:
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


def find_the_best_geoids(max_time: int, ore_robot_cost_ore: int, clay_robot_cost_ore: int, obsidian_robot_cost_ore: int, obsidian_robot_cost_clay: int, geode_robot_cost_ore: int, geode_robot_cost_obsidian: int) -> int:
    todo = [(max_time,  0, 0, 0, 0,  1, 0, 0, 0)]
    seen = set()

    max_obsidians_obtains = 0

    max_ore_robots = max(ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, geode_robot_cost_ore)
    max_clay_robots = obsidian_robot_cost_clay
    max_obsidian_robots = geode_robot_cost_obsidian

    while todo:
        time, ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots = todo.pop()
        if time < 0 or (ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots) in seen:
            continue

        geodes_on_the_timeout = geode + time * geode_robots
        if (geodes_on_the_timeout + time * (time - 1) // 2) <= max_obsidians_obtains:
            continue

        max_obsidians_obtains = max(geodes_on_the_timeout, max_obsidians_obtains)
        seen.add((ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots))

        # ore robot
        if time > 2 and ore_robots < max_ore_robots:
            if ore < time * max_ore_robots:
                time_to_purchase = calculate_time_to_purchase(ore, ore_robots, ore_robot_cost_ore)
                if time > time_to_purchase:
                    todo.append((
                        time - time_to_purchase,

                        ore + ore_robots * time_to_purchase - ore_robot_cost_ore,
                        clay + clay_robots * time_to_purchase,
                        obsidian + obsidian_robots * time_to_purchase,
                        geode + geode_robots * time_to_purchase,
                        
                        ore_robots + 1, clay_robots, obsidian_robots, geode_robots
                    ))

        # clay robot
        if time > 2 and clay_robots < max_clay_robots:
            if clay < time * max_clay_robots:
                time_to_purchase = calculate_time_to_purchase(ore, ore_robots, clay_robot_cost_ore)
                if time > time_to_purchase:
                    todo.append((
                        time - time_to_purchase,

                        ore + time_to_purchase * ore_robots - clay_robot_cost_ore,
                        clay + time_to_purchase * clay_robots,
                        obsidian + obsidian_robots * time_to_purchase,
                        geode + geode_robots * time_to_purchase,
                        
                        ore_robots, clay_robots + 1, obsidian_robots, geode_robots
                    ))

        # obsidian robot
        if time > 2 and clay_robots > 0 and obsidian_robots < max_obsidian_robots:
            if obsidian < time * max_obsidian_robots:
                time_to_purchase = max(
                    calculate_time_to_purchase(ore, ore_robots, obsidian_robot_cost_ore),
                    calculate_time_to_purchase(clay, clay_robots, obsidian_robot_cost_clay))
                if time > time_to_purchase:
                    todo.append((
                        time - time_to_purchase,

                        ore + time_to_purchase * ore_robots - obsidian_robot_cost_ore,
                        clay + time_to_purchase * clay_robots - obsidian_robot_cost_clay,
                        obsidian + obsidian_robots * time_to_purchase,
                        geode + geode_robots * time_to_purchase,

                        ore_robots, clay_robots, obsidian_robots + 1, geode_robots
                    ))

        # geode robot
        if time > 1 and obsidian_robots > 0:
            time_to_purchase = max(
                calculate_time_to_purchase(ore, ore_robots, geode_robot_cost_ore),
                calculate_time_to_purchase(obsidian, obsidian_robots, geode_robot_cost_obsidian))
            if time > time_to_purchase:
                todo.append((
                    time - time_to_purchase,

                    ore + time_to_purchase * ore_robots - geode_robot_cost_ore,
                    clay + time_to_purchase * clay_robots,
                    obsidian + obsidian_robots * time_to_purchase - geode_robot_cost_obsidian,
                    geode + geode_robots * time_to_purchase,

                    ore_robots, clay_robots, obsidian_robots, geode_robots + 1
                ))

    return max_obsidians_obtains


def solution_for_first_part(task_input: Iterable[str]) -> int:
    return sum(
        id * find_the_best_geoids(24, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian)
        for id, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian in parse(task_input))


example_input = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''.splitlines()

assert solution_for_first_part(example_input) == 33
# The input is taken from: https://adventofcode.com/2022/day/19/input
task_input = list(load_input_file('input.19.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: Iterable[str]) -> int:
    left_blueprints = list(parse(task_input))[:3]

    return reduce(
        mul,
        (
            find_the_best_geoids(32, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian)
            for _, ore_robot_cost_ore, clay_robot_cost_ore, obsidian_robot_cost_ore, obsidian_robot_cost_clay, geode_robot_cost_ore, geode_robot_cost_obsidian in left_blueprints
        ))


example_blueprint_1, example_blueprint_2 = parse(example_input)
assert find_the_best_geoids(32, *(tuple(example_blueprint_1)[1:])) == 56
assert find_the_best_geoids(32, *(tuple(example_blueprint_2)[1:])) == 62

print("Solution for the second part:", solution_for_second_part(task_input))
