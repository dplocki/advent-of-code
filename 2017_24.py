def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def joints(lines: [str]) -> {int:set}:

    def parse_input(lines: [str]):
        for line in lines:
            yield tuple(map(int, line.split('/')))

    return [(x, y) for x, y in parse_input(lines)]


def find_all_matching_joints(joints: [tuple], ending: int):
    return [join for join in joints if join[0] == ending or join[1] == ending]


def build_brigdes(joints: [tuple], path: [], ending: int):
    for joint in find_all_matching_joints(joints, ending):
   
        path.append(joint)
        yield path

        joints.remove(joint)

        yield from build_brigdes(
            joints,
            path,
            joint[0] if joint[1] == ending else joint[1]
        )

        joints.append(joint)
        path.pop()


def cost_of(path):
    return sum([x + y for x, y in path])


def solution_for_first_part(lines: [str]):
    return max([
        cost_of(path)
        for path in build_brigdes(joints(lines), [], 0)
    ])


test_input = '''0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10'''

assert solution_for_first_part(test_input.splitlines()) == 31

print("Solution for the first part:", solution_for_first_part(file_to_input_list('input.24.txt')))
