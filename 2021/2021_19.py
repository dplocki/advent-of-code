from itertools import combinations
from typing import Callable


REQUIRED_BECON_OVERLAP = 12
X, Y, Z = 0, 1, 2


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().strip()


def parse(task_input: str) -> dict[int, list[tuple[int, int, int]]]:
    scanners = task_input.split('\n\n')

    result = {}
    for index, scanner in enumerate(scanners):
        becons_lines = scanner.splitlines()
        result[index] = [tuple(map(int, line.split(','))) for line in becons_lines[1:]]

    return result


def distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2])


class BeconDistance():

    def __init__(self, *points) -> None:
        self.points = points
        self.distances = set(tuple(sorted(distance(a, b))) for a, b in combinations(points, 2))

    def __hash__(self):
        return sum(sum(d) for d in self.distances)

    def __eq__(self, other) -> bool:
        return self.distances == other.distances


def find_all_beacons(task_input: list[str]) -> list[tuple[int, int, int]]:


    def transform_point(transformation_matrix: dict[tuple[int, int], int], point: tuple[int, int, int]) -> tuple[int, int, int]:
        result = [0, 0, 0, 0]
        vector = [*point, 1]

        for y in range(0, 4):
            for x in range(0, 4):
                result[y] += transformation_matrix[x, y] * vector[x]

        return result[X], result[Y], result[Z]


    def match_from(points, distances):
        for p1 in points:
            curent_distances = set(BeconDistance(p1, p2) for p2 in points if p1 != p2)
            if curent_distances == distances:
                return p1

        raise Exception('Unable to find the matching point')


    def calculate_transform_function(points: list[tuple[tuple[int, int, int], tuple[int, int, int]]]) -> Callable:
        A_POINT, B_POINT = 0, 1
        FIRST_PAIR, SECOND_PAIR = 0, 1


        def calculate_multiplayer(sa_p1: int, sb_p1: int, sa_p2: int, sb_p2: int) -> int:
            if (sa_p1 > sa_p2 and sb_p1 > sb_p2) or (sa_p1 < sa_p2 and sb_p1 < sb_p2):
                return 1

            if (sa_p1 > sa_p2 and sb_p1 < sb_p2) or (sa_p1 < sa_p2 and sb_p1 > sb_p2):
                return -1

            raise Exception('two points on equal coordinates')


        def make_transformation_matrix(x_index, y_index, z_index):
            result_matrix = {(x,y):0 for x in range(4) for y in range(4)}
            result_matrix[3, 3] = 1

            result_matrix[x_index, X] = calculate_multiplayer(points[FIRST_PAIR][A_POINT][X], points[FIRST_PAIR][B_POINT][x_index], points[SECOND_PAIR][A_POINT][X], points[SECOND_PAIR][B_POINT][x_index])
            result_matrix[y_index, Y] = calculate_multiplayer(points[FIRST_PAIR][A_POINT][Y], points[FIRST_PAIR][B_POINT][y_index], points[SECOND_PAIR][A_POINT][Y], points[SECOND_PAIR][B_POINT][y_index])
            result_matrix[z_index, Z] = calculate_multiplayer(points[FIRST_PAIR][A_POINT][Z], points[FIRST_PAIR][B_POINT][z_index], points[SECOND_PAIR][A_POINT][Z], points[SECOND_PAIR][B_POINT][z_index])

            result_matrix[3, X] = points[FIRST_PAIR][A_POINT][X] - result_matrix[x_index, X] * points[FIRST_PAIR][B_POINT][x_index]
            result_matrix[3, Y] = points[FIRST_PAIR][A_POINT][Y] - result_matrix[y_index, Y] * points[FIRST_PAIR][B_POINT][y_index]
            result_matrix[3, Z] = points[FIRST_PAIR][A_POINT][Z] - result_matrix[z_index, Z] * points[FIRST_PAIR][B_POINT][z_index]

            return result_matrix

        global distance

        x, y, z = distance(points[FIRST_PAIR][A_POINT], points[SECOND_PAIR][A_POINT])

        if distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (x, y, z):
            result_matrix = make_transformation_matrix(X, Y, Z)
        elif distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (y, z, x):
            result_matrix = make_transformation_matrix(Z, X, Y)
        elif distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (y, x, z):
            result_matrix = make_transformation_matrix(Y, X, Z)
        elif distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (z, x, y):
            result_matrix = make_transformation_matrix(Y, Z, X)
        elif distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (x, z, y):
            result_matrix = make_transformation_matrix(X, Z, Y)
        elif distance(points[FIRST_PAIR][B_POINT], points[SECOND_PAIR][B_POINT]) == (z, y, x):
            result_matrix = make_transformation_matrix(Z, Y, X)

        assert transform_point(result_matrix, points[FIRST_PAIR][B_POINT]) == points[FIRST_PAIR][A_POINT]
        assert transform_point(result_matrix, points[SECOND_PAIR][B_POINT]) == points[SECOND_PAIR][A_POINT]

        return result_matrix


    def only_overlapping_points(commons_points, scanners_points_distances):
        result = set()
        for x in scanners_points_distances:
            if x in commons_points:
                result.add(x.points[0])
                result.add(x.points[1])

        return result


    def find_scanners_order(scanners_points_distances: dict[int, set[BeconDistance]], start: int) -> list[int]:
        REQUIRED_PAIRS_NUMBER = REQUIRED_BECON_OVERLAP * (REQUIRED_BECON_OVERLAP - 1) // 2
        result = [start]
        posibilites = [start]

        scanners_overlaps = [(scanner_a, scanner_b)
            for scanner_a, scanner_b in combinations(scanners_points_distances.keys(), 2)
            if len(scanners_points_distances[scanner_a] & scanners_points_distances[scanner_b]) == REQUIRED_PAIRS_NUMBER]

        while posibilites:
            current = posibilites.pop()

            for a, b in scanners_overlaps:
                if current == a and b not in result:
                    posibilites.append(b)
                    result.append(b)

                if current == b and a not in result:
                    posibilites.append(a)
                    result.append(a)

        return result


    scanners = parse(task_input)
    scanners_points_distances = {
        scanner_index: {BeconDistance(a, b) for a, b in combinations(scanner_readings, 2)}
        for scanner_index, scanner_readings in scanners.items()}
    
    scanners_order = find_scanners_order(scanners_points_distances, 0)[1:]

    all_beacons = set(becon for becon in scanners[0])
    all_beacons_distances = set()
    all_beacons_distances.update(scanners_points_distances[0])
    scanners_from_0 = [(0, 0, 0)]

    for scanner_number in scanners_order:
        commons_points = all_beacons_distances & scanners_points_distances[scanner_number]

        overlapping_points_from_a = only_overlapping_points(commons_points, all_beacons_distances)
        overlapping_points_from_b = only_overlapping_points(commons_points, scanners_points_distances[scanner_number])
        
        points_from_scanner_zero = []
        for _, point_from_a in zip(range(2), overlapping_points_from_a):
            distances_of_point_from_a = set(BeconDistance(point_from_a, point) for point in overlapping_points_from_a if point_from_a != point)
            points_from_scanner_zero.append((point_from_a, match_from(overlapping_points_from_b, distances_of_point_from_a)))

        translation_matrix = calculate_transform_function(points_from_scanner_zero)

        for beacon in scanners[scanner_number]:
            all_beacons.add(transform_point(translation_matrix, beacon))

        for distance in scanners_points_distances[scanner_number]:
            distance.points = [transform_point(translation_matrix, point) for point in distance.points]
            all_beacons_distances.add(distance)

        scanners_from_0.append(transform_point(translation_matrix, (0, 0, 0)))


    return all_beacons, scanners_from_0


def solution_for_first_part(all_beacons: list[tuple[int, int, int]]) -> int:
    return len(all_beacons)


example_input = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''

all_example_beacons, all_example_scanners = find_all_beacons(example_input)
assert solution_for_first_part(all_example_beacons) == 79

# The input is taken from: https://adventofcode.com/2021/day/19/input
all_input_beacons, all_input_scanners = find_all_beacons(load_input_file('input.19.txt'))
print("Solution for the first part:", solution_for_first_part(all_input_beacons))


def solution_for_second_part(all_scanners: list[tuple[int, int, int]]) -> int:
    return max(sum(distance(a, b)) for a, b in combinations(all_scanners, 2))


assert solution_for_second_part(all_example_scanners) == 3621
print("Solution for the second part:", solution_for_second_part(all_input_scanners))
