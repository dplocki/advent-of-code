UP, DOWN, RIGTH, LEFT = 11, 22, 33, 44
CLEAN, WEEKENED, INFECTED, FLAGGED = 19, 29, 39, 49


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_input(lines: [str]):
    start_x = 0
    x, y = 0, 0
    size = None

    for line in lines:
        if not size:
            size = len(line)
            start_x = 0 - size // 2
            y = 0 - size // 2

        x = start_x
        for char in line:
            if char == '#':
                yield (x, y)

            x += 1
        y += 1


class Cluster():

    def __init__(self, initial_input: [str]):
        self.build_nodes(initial_input)
        self.result = 0
        self.position = (0, 0)
        self.oriented = UP

    def build_nodes(self, initial_input):
        self.nodes = set()
        for p in parse_input(initial_input):
            self.nodes.add(p) 

    def get_current_node_state(self):
        return INFECTED if self.position in self.nodes else CLEAN

    def transform_direction(self):
        current_node_state = self.get_current_node_state()

        if current_node_state == INFECTED:
            # right
            if self.oriented == UP:
                self.oriented = RIGTH
            elif self.oriented == DOWN:
                self.oriented = LEFT        
            elif self.oriented == RIGTH:
                self.oriented = DOWN
            elif self.oriented == LEFT:
                self.oriented = UP
        elif current_node_state == CLEAN:
            # left
            if self.oriented == UP:
                self.oriented = LEFT
            elif self.oriented == DOWN:
                self.oriented = RIGTH        
            elif self.oriented == RIGTH:
                self.oriented = UP
            elif self.oriented == LEFT:
                self.oriented = DOWN
        elif current_node_state == WEEKENED:
                 self.oriented = self.oriented
        elif current_node_state == FLAGGED:
            if self.oriented == UP:
                self.oriented = DOWN
            elif self.oriented == DOWN:
                self.oriented = UP        
            elif self.oriented == RIGTH:
                self.oriented = LEFT
            elif self.oriented == LEFT:
                self.oriented = RIGTH
        else:
            raise "Unexcepted!"

    def move(self):
        if self.oriented == UP:
            self.position = (self.position[0], self.position[1] - 1)
        elif self.oriented == DOWN:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.oriented == RIGTH:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.oriented == LEFT:
            self.position = (self.position[0] - 1, self.position[1])

    def transform_node(self):
        if self.position in self.nodes:
            self.nodes.remove(self.position)
        else:
            self.nodes.add(self.position)
            self.result += 1

    def step_generator(self):
        while True:
            self.transform_direction()
            self.transform_node()
            self.move()

            yield self.result


class EvolvedCluster(Cluster):

    def __init__(self, initial_input: [str]):
        Cluster.__init__(self, initial_input)

    def build_nodes(self, initial_input):
        self.nodes = {}
        for p in parse_input(initial_input):
            self.nodes[p] = INFECTED

    def get_current_node_state(self):
        return self.nodes.get(self.position, CLEAN)

    def transform_node(self):
        if self.position in self.nodes:
            state = self.nodes[self.position]

            if state == WEEKENED:
                self.nodes[self.position] = INFECTED
                self.result += 1
            elif state == INFECTED:
                self.nodes[self.position] = FLAGGED
            elif state == FLAGGED:
                del self.nodes[self.position]
            else:
                raise "Unexcepted!"
        else:
            self.nodes[self.position] = WEEKENED


def run_generator_n_times(cluster: Cluster, n: int):
    generator = cluster.step_generator()
    for result, _ in zip(generator, range(n)):
        pass

    return result


test_input = '''..#
#..
...'''.splitlines()

assert run_generator_n_times(Cluster(test_input), 70) == 41
assert run_generator_n_times(Cluster(test_input), 10000) == 5587

# The input is taken from https://adventofcode.com/2017/day/22/input
print("The solution for the first part:", run_generator_n_times(Cluster(file_to_input_list('input.22.txt')), 10000))

assert run_generator_n_times(EvolvedCluster(test_input), 100) == 26
assert run_generator_n_times(EvolvedCluster(test_input), 10_000_000) == 2511944

print("The solution for the second part:", run_generator_n_times(EvolvedCluster(file_to_input_list('input.22.txt')), 10000000))
