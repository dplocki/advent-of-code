from typing import Dict, Generator, Iterable, Set
from networkx import Graph, minimum_edge_cut


def load_input_file(file_name: str) -> Generator[str, None, None]:
    with open(file_name) as file:
        yield from (line.rstrip() for line in file)


def build_graph(task_input: Iterable[str]) -> Dict[str, Set[str]]:
    result = {}

    for line in task_input:
        nodes = line.replace(': ', ' ').split(' ')

        neighbors = result.get(nodes[0], set())
        neighbors.update(nodes[1:])
        result[nodes[0]] = neighbors

        for node in nodes[1:]:
            neighbors = result.get(node, set())
            neighbors.add(nodes[0])
            result[node] = neighbors

    return result


def solution_for_first_part(task_input: Iterable[str]) -> int:
    graph = build_graph(task_input)
    vertexes = set()
    edges = set()

    for node, neighbors in graph.items():
        vertexes.add(node)
        vertexes.update(neighbors)

        for neighbor in neighbors:
            edges.add(tuple(sorted((node, neighbor))))

    vertex_numeric = {}
    for i, neighbors in enumerate(vertexes):
        vertex_numeric[neighbors] = i

    G = Graph()
    for node_a, node_b in edges:
        G.add_edge(node_a, node_b)

    edges_to_remove = minimum_edge_cut(G)
    for node_a, node_b in edges_to_remove:
        G.remove_edge(node_a, node_b)

    to_check = set()
    to_check.add(next(iter(G.nodes())))
    cluster = set()

    while to_check:
        edges_to_remove = to_check.pop()
        if edges_to_remove in cluster:
            continue

        cluster.add(edges_to_remove)
        for neighbor in G.neighbors(edges_to_remove):
            to_check.add(neighbor)

    return len(cluster) * (len(vertexes) - len(cluster))


example_input = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''.splitlines()

assert solution_for_first_part(example_input) == 54

# The input is taken from: https://adventofcode.com/2023/day/25/input
task_input = list(load_input_file('input.25.txt'))
print("Solution for the first part:", solution_for_first_part(task_input))
