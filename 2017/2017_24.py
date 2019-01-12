TESTING = False


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def cost_of(path):
    return sum([x + y for x, y in path])


def build_all_bidges(lines: [str]):


    def find_all_matching_joints(joints: [tuple], ending: int):
        return [join for join in joints if join[0] == ending or join[1] == ending]


    def parse_joints(lines: [str]):
        for line in lines:
            yield tuple(map(int, line.split('/')))


    def build_brigdes(joints: list, path: list, ending: int):
        for joint in find_all_matching_joints(joints, ending):
            path.append(joint)

            yield path[:]

            joints.remove(joint)

            yield from build_brigdes(
                joints,
                path,
                joint[0] if joint[1] == ending else joint[1]
            )

            joints.append(joint)
            path.pop()


    return list(build_brigdes(list(parse_joints(lines)), [], 0))


def solution_for_first_part(brigdes: [[int]]):
    return max([cost_of(brigde) for brigde in brigdes])


def solution_for_second_part(brigdes: [[int]]):
    the_longest_lenght = max([len(brigde) for brigde in brigdes])

    return max([
        cost_of(bridge)
        for bridge in brigdes
        if len(bridge) == the_longest_lenght
    ])


if TESTING:

    test_input = '''0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10'''

    test_bridges = build_all_bidges(test_input.splitlines())
    assert solution_for_first_part(test_bridges) == 31
    assert solution_for_second_part(test_bridges) == 19

else:
    
    # The input taken from https://adventofcode.com/2017/day/24/input
    bridges = build_all_bidges(file_to_input_list('input.24.txt'))
    print("Solution for the first part:", solution_for_first_part(bridges))
    print("Solution for the second part:", solution_for_second_part(bridges))
