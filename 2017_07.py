import re


def parse_file(file_name):
    pattern = re.compile(r'^([a-z]+) \(([0-9]+)\)( -> ([a-z, ]+))?\n$')

    with open(file_name) as file:
        for line in file:
            result = pattern.match(line)
            yield (result[1], int(result[2]), result[4].split(', ') if result[4] else [])


class Node:
    def __init__(self, weight, children_names):
        self.weight = weight
        self.children: [Node] = children_names
        self.weight_with_children = None


def builds_nodes(collection):
    nodes = {}
    only_parents = []

    for _ in collection:
        nodes[_[0]] = Node(_[1], _[2])

        if _[2]:
            only_parents.append(_[0])

    return nodes, only_parents


def find_root(nodes, only_parents):

    def is_child(name):
        for parent in only_parents:
            if name in nodes[parent].children:
                return True

        return False

    for name, _ in nodes.items():
        if not is_child(name):
            return name

    return None


def get_whole_node_weight(nodes: [Node], node: Node):
    if not node.weight_with_children:
        result = node.weight

        for child in node.children:
            result += get_whole_node_weight(nodes, nodes[child])

        node.weight_with_children = result

    return node.weight_with_children


def recalculate_node_weights(nodes):
    for _, node in nodes.items():
        node.weight_with_children = get_whole_node_weight(nodes, node)

    return nodes


def the_most_common(lst):
    return max(set(lst), key=lst.count)


def seek_unbalanced_node(nodes, only_parents):
    for only_parent in only_parents:
        node = nodes[only_parent]
        children_weigths = [nodes[child].weight_with_children for child in node.children]

        if len(set(children_weigths)) > 1:
            normal = the_most_common(children_weigths)

            for child_name in node.children:
                child = nodes[child_name]
                if child.weight_with_children == normal:
                    continue

                return abs(child.weight - abs(child.weight_with_children - normal))


nodes, only_parents = builds_nodes(parse_file('input.txt'))
nodes = recalculate_node_weights(nodes)

print("Root: ", find_root(nodes, only_parents))
print("To balance one should have: ", seek_unbalanced_node(nodes, only_parents))
