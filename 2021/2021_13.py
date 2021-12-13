def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> tuple[set[tuple[int, int]], tuple[str, int]]:
    task_input_parts = task_input.split('\n\n')

    points = set(tuple(map(int, line.split(','))) for line in task_input_parts[0].splitlines())
    folds = []
    for line in task_input_parts[1].splitlines():
        tokens = line.split('=')
        folds.append((tokens[0][-1], int(tokens[1])))

    return points, folds


def apply_fold_horizontal(points: set, fold_y: int) -> set:
    result = set()
    for point in points:
        if point[1] < fold_y:
            result.add(point)

        if point[1] > fold_y:
            result.add((point[0], fold_y - (point[1] - fold_y)))

    return result


def apply_fold_vertical(points: set, fold_x: int) -> set:
    result = set()
    for point in points:
        if point[0] < fold_x:
            result.add(point)

        if point[0] > fold_x:
            result.add((fold_x - (point[0] - fold_x), point[1]))

    return result


def fold_paper(task_input: str) -> list[set]:
    points, folds = parse(task_input)

    for how_fold, fold_line in folds:
        if how_fold == 'x':
            points = apply_fold_vertical(points, fold_line)

        elif how_fold == 'y':
            points = apply_fold_horizontal(points, fold_line)

        else:
            raise Exception('Unknow folding way')

        yield points


def solution_for_first_part(task_input: str) -> int:
    one_fold = next(fold_paper(task_input))
    return len(one_fold)


example_input = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

# assert solution_for_first_part(example_input) == 17

# # The input is taken from: https://adventofcode.com/2021/day/13/input
task_input = load_input_file('input.13.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input) -> int:

    def visualization(points):
        xs = [x for x, _ in points]
        ys = [y for _, y in points]
        max_x = max(xs)
        max_y = max(ys)
        min_x = min(xs)
        min_y = min(ys)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print('#' if (x, y) in points else '.', end='')

            print()


    for fold in fold_paper(task_input):
        pass

    visualization(fold)


solution_for_second_part(example_input)
print("Solution for the second part:")
solution_for_second_part(task_input)
