def load_input_file(file_name):
    with open(file_name) as file:
        yield from (line.strip() for line in file)


def parse(lines):
    for line in lines:
        yield list(map(lambda x: int(x), line.split()))


def find_all_posible_triangles(trinagles_list: [[int]]) -> int:
    result = 0
    for raw_trinagle in trinagles_list:
        trinagle = sorted(raw_trinagle)
        if trinagle[2] < trinagle[0] + trinagle[1]:
            result += 1

    return result


def transform_list(input_list: [[int]]) -> [[int]]:
    triangle_1 = []
    triangle_2 = []
    triangle_3 = []

    for t1, t2, t3 in input_list:
        triangle_1.append(t1)
        triangle_2.append(t2)
        triangle_3.append(t3)

        if len(triangle_1) == 3:
            yield triangle_1
            yield triangle_2
            yield triangle_3

            triangle_1 = []
            triangle_2 = []
            triangle_3 = []
        

def solution_for_second_part(input_list: [[int]]) -> int:
    return find_all_posible_triangles(transform_list(input_list))

# The input is taken from: https://adventofcode.com/2016/day/3/input
input_list = list(parse(load_input_file('input.03.txt')))
print("Solution for the first part:", find_all_posible_triangles(input_list))
print("Solution for the second part:", solution_for_second_part(input_list))
