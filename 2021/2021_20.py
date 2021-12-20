LIGHT_PIXEL = '#'


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: list[str]) -> tuple[list[str], dict[tuple[int, int], str]]:
    enhance_token, image_token = task_input.split('\n\n')

    enhance = [character == LIGHT_PIXEL for character in enhance_token]
    image = set((x, y)
        for y, line in enumerate(image_token.splitlines())
        for x, value in enumerate(line) if value == LIGHT_PIXEL)

    return enhance, image


def get_eight_neighbors(x: int, y: int) -> list[tuple[int, int]]:
    yield (x + 1, y + 1) # SE
    yield (x, y + 1)     # S
    yield (x - 1, y + 1) # SW

    yield (x + 1, y)     # E
    yield (x, y)
    yield (x - 1, y)     # W
    
    yield (x + 1, y - 1) # NE
    yield (x, y - 1)     # N
    yield (x - 1, y - 1) # NW


def enhance_image(enhance: list[str], image: dict[tuple[int, int], str], is_background_light: str) -> dict[tuple[int, int], str]:
    xs = [x for x, _ in image]
    ys = [y for _, y in image]
    
    max_x = max(xs)
    max_y = max(ys)
    min_x = min(xs)
    min_y = min(ys)
    
    new_image = set()
    for y in range(min_y - 2, max_y + 3):
        for x in range(min_x - 2 , max_x + 3):

            value = 0
            multiplayer = 1
            for p in get_eight_neighbors(x, y):
                if min_x <= p[0] <= max_x and min_y <= p[1] <= max_y:
                    if p in image:
                        value += multiplayer
                elif is_background_light:
                    value += multiplayer

                multiplayer <<= 1

            if enhance[value]:
                new_image.add((x, y))

    return new_image


def solution_for_first_part(task_input: str) -> int:
    enhance, image = parse(task_input)

    image = enhance_image(enhance, image, False)
    image = enhance_image(enhance, image, enhance[0])

    return len(image)


example_input = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

assert solution_for_first_part(example_input) == 35

# The input is taken from: https://adventofcode.com/2021/day/20/input
task_input = load_input_file('input.20.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


def solution_for_second_part(task_input: str) -> int:
    enhance, image = parse(task_input)

    for _ in range(25):
        image = enhance_image(enhance, image, False)
        image = enhance_image(enhance, image, enhance[0])

    return len(image)


assert solution_for_second_part(example_input) == 3351
print("Solution for the second part:", solution_for_second_part(task_input))
