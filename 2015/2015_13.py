import re


def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def build_grap(lines: [str]) -> dict:


    def parse_input(lines: [str]):
        pattern = re.compile(r'(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+).')
        for line in lines:
            groups = pattern.match(line)
            yield groups[1], (-1 if groups[2] == 'lose' else 1) * int(groups[3]), groups[4]


    result = {}
    for who, how_much, to_whom in parse_input(lines):
        tmp = result.get(who, {})
        tmp[to_whom] = how_much
        result[who] = tmp

    return result


def find_maximum_happines_level(graph: {}) -> int:


    def generate_paths(graph: {}, from_person: str, taken_seats: [], current_happiness_level: int):
        posible_neigborns = set(person for person in graph[from_person].keys() if person not in taken_seats)

        if posible_neigborns:
            for neigborn in posible_neigborns:
                taken_seats.append(neigborn)

                level_delta = graph[from_person][neigborn] + graph[neigborn][from_person]

                yield from generate_paths(
                        graph,
                        neigborn,
                        taken_seats,
                        current_happiness_level + level_delta)

                taken_seats.remove(neigborn)
        else:
            current_happiness_level += graph[from_person][taken_seats[0]]  # circle is closing
            current_happiness_level += graph[taken_seats[0]][from_person]
            
            yield current_happiness_level


    first = next(graph.keys().__iter__())
    return max(happiness_level for happiness_level in generate_paths(graph, first, [first], 0))


def solution_for_first_part(graph: {}) -> int:
    return find_maximum_happines_level(graph)


def solution_for_second_part(graph: {}) -> int:
    people = graph.keys()
    for person in people:
        graph[person]['Me'] = 0

    graph['Me'] = {person:0 for person in people}
    
    return find_maximum_happines_level(graph)


test_input = '''Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.'''


test_graph = build_grap(test_input.splitlines())
assert solution_for_first_part(test_graph) == 330

# The solution is taken from: https://adventofcode.com/2015/day/13/input
graph = build_grap(load_input_file('input.13.txt'))

print("Solution for the first part:", solution_for_first_part(graph))
print("Solution for the second part:", solution_for_second_part(graph))
