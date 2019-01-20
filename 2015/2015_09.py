
def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def solution_for_the_part(lines_provider: [str]):


    def build_graph(lines_provider: [str]):
        result = {}

        for line in lines_provider:
            (label, distance) = line.split(' = ')
            (_from, _to) = label.split(' to ')
            distance = int(distance)

            e1 = result.get(_from, {})
            e1[_to] = distance
            result[_from] = e1

            e2 = result.get(_to, {})
            e2[_from] = distance
            result[_to] = e2

        return result


    def generate_paths(graph: {}, from_city: str, path: [], current_cost: int):
        next_cities = set(city for city in graph[from_city].keys() if city not in path)
        if next_cities:
            for to_city in next_cities:
                path.append(to_city)

                yield from generate_paths(graph, to_city, path, current_cost + graph[from_city][to_city])

                path.remove(to_city)
        else:
            yield current_cost


    graph = build_graph(lines_provider)

    return min(distance for city in graph.keys() for distance in generate_paths(graph, city, [city], 0))


test_input = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''

assert solution_for_the_part(test_input.splitlines()) == 605

# The solution is taken from: https://adventofcode.com/2015/day/9/input
print("Solution for the first part:", solution_for_the_part(load_input_file('input.09.txt')))
