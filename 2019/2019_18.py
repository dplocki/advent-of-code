def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def read_maze(raw_maze: [str]):
    maze = {}
    start_position = None
    keys = {}

    for y, line in enumerate(raw_maze):
        for x, c in enumerate(line):
            maze[(x, y)] = c if c != '@' else '.'
            start_position = (x, y) if c == '@' else start_position
            if c.isalpha():
                if not c.isupper():
                    keys[c.lower()] = (x, y)

    return maze, start_position, keys


def get_paths_metadata_to_other_keys(maze: dict, start: tuple, keys: dict):
    
    def is_door(maze, position):
        return maze[position].isalpha() and maze[position].isupper()

    def get_neigborn(maze: dict, where: tuple):
        x, y = where
        for position in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if position in maze:
                tile = maze[position]
                if tile != '#':
                    yield position

    visited = {}
    posibilities = [(start, 0, set())]

    while posibilities:
        position, steps, needed_keys = posibilities.pop(0)
        visited[position] = (steps, needed_keys.copy())

        if is_door(maze, position):
            needed_keys.add(maze[position].lower())

        next_steps = steps + 1
        for next_position in get_neigborn(maze, position):
            if next_position in visited:
                s, _ = visited[next_position]
                if next_steps < s:
                    visited[next_position] = (next_steps, needed_keys)
                continue

            posibilities.append((next_position, next_steps, needed_keys.copy()))

    return {key_name:(visited[key_position][0], visited[key_position][1]) for key_name, key_position in keys.items() if key_position != start}


def get_path_length(paths_metadata, keys_positions, start_position):
    possibilities = [(start_position, 0, set())]
    cache = {}

    while possibilities:
        current_position, length, own_keys = possibilities.pop()

        if len(own_keys) == len(keys_positions):
            yield length
            continue

        path_hash = ''.join(sorted(own_keys))
        if (current_position, path_hash) in cache:
            result = cache[current_position, path_hash]
            if result <= length:
                continue

        cache[current_position, path_hash] = length

        for key_name, metadata in paths_metadata[current_position].items():
            join_length, need_keys = metadata
            if not key_name in own_keys and need_keys.issubset(own_keys):
                possibilities.append((
                        keys_positions[key_name],
                        length + join_length,
                        own_keys.union([key_name])
                    ))


def solution_for_first_part(input: [str]):
    maze, start_position, keys_positions = read_maze(input)

    path_metadata = {
            position: get_paths_metadata_to_other_keys(maze, position, keys_positions)
            for position in ([start_position] + list(keys_positions.values()))
        }

    return min(get_path_length(path_metadata, keys_positions, start_position))


assert solution_for_first_part('''#########
#b.A.@.a#
#########'''.splitlines()) == 8

assert solution_for_first_part('''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################'''.splitlines()) == 86

assert solution_for_first_part('''########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################'''.splitlines()) == 132

assert solution_for_first_part('''#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################'''.splitlines()) == 136

assert solution_for_first_part('''########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################'''.splitlines()) == 81

#The input is taken from: https://adventofcode.com/2019/day/18/input
print("Solution for the first part:", solution_for_first_part(load_input_file('input.18.txt')))
