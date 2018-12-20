def recreate_doors(input):
    doors = set()

    current_point = (0, 0)
    queue = []

    for character in input:
        if character in '^$':
            continue
        elif character == 'N':  # north
            doors.add((current_point[0], current_point[1] - 1))
            current_point = (current_point[0], current_point[1] - 2)
        elif character == 'S':  # south
            doors.add((current_point[0], current_point[1] + 1))
            current_point = (current_point[0], current_point[1] + 2)
        elif character == 'W':  # west
            doors.add((current_point[0] - 1, current_point[1]))
            current_point = (current_point[0] - 2, current_point[1])
        elif character == 'E':  # east
            doors.add((current_point[0] + 1, current_point[1]))
            current_point = (current_point[0] + 2, current_point[1])

        elif character == '(':
            queue.append(current_point)

        elif character == '|':
            current_point = queue[-1]

        elif character == ')':
            current_point = queue.pop()

        else:
            raise("Uknown!")

    return doors


def visualisation(doors: set):
    min_y = min(doors, key=lambda x: x[1])[1] - 2
    max_y = max(doors, key=lambda x: x[1])[1] + 3

    min_x = min(doors, key=lambda x: x[0])[0] - 2
    max_x = max(doors, key=lambda x: x[0])[0] + 3

    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in doors:
                if x % 2 == 0:
                    print('-', end='')
                else:
                    print('|', end='')
            else:
                if x == 0 and y == 0:
                    print('X', end='')
                elif x % 2 == 0 and y % 2 == 0:
                    print('.', end='')
                else:
                    print('#', end='')

        print('\n', end='')


def get_neighborns(doors: set, point):
    return [
        (point[0] + i[0] + i[0], point[1] + i[1] + i[1])
        for i in [(0, -1), (0, 1), (1, 0), (-1, 0)]
        if (point[0] + i[0], point[1] + i[1]) in doors
    ]


def find_the_longest_path(doors: set):
    frontier = [(0, 0)]
    distance = {}
    distance[(0, 0)] = 0

    while frontier:
        current = frontier.pop()
        
        new_path = distance[current] + 1
        for next in get_neighborns(doors, current):
            if next not in distance:
                frontier.append(next)
                distance[next] = new_path

    return max(distance.values())


assert recreate_doors('^WNE$') == set([(-1, 0), (-2, -1), (-1, -2)])

test_doors_set_1 = recreate_doors('^N(E|W)N$')
visualisation(recreate_doors('^N(E|W)N$'))

assert test_doors_set_1 == set([(0, -1), (1, -2), (0, -3), (-1, -2)])
assert get_neighborns(test_doors_set_1, (0, 0)) == [(0, -2)]
assert get_neighborns(test_doors_set_1, (0, -2)) == [(0, -4), (0, 0), (2, -2), (-2, -2)]

test_doors_set_2 = recreate_doors('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')
assert find_the_longest_path(test_doors_set_2) == 23

test_doors_set_3 = recreate_doors('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')
assert find_the_longest_path(test_doors_set_3) == 31


# The input taken from https://adventofcode.com/2018/day/20/input
input = '<input>'

print("Solution for first part:", find_the_longest_path(recreate_doors(input)))
