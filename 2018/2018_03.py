import re


def file_to_input_list(file_name):
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def parse_lines(lines):
    pattern = re.compile(r'^\#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
    for line in lines:
        match = pattern.match(line)
        yield int(match[2]), int(match[3]), int(match[4]), int(match[5]), int(match[1])


def cuts_to_indexes(fabric_size, cuts: []):
    for cut in cuts:
        for x in range(cut[2]):
            for y in range(cut[3]):
                yield ((cut[1] + y)*fabric_size + cut[0] + x), cut[4]


def build_fabric(fabric_size: int) -> []:
    return [0] * (fabric_size ** 2)


def count_overlaps_for_fabric_by_cuts(fabric_size: int, cuts: []) -> int:
    fabric = build_fabric(fabric_size)

    for index, _ in cuts_to_indexes(fabric_size, parse_lines(cuts)):
        fabric[index] += 1

    return sum(f > 1 for f in fabric)


def find_non_overlaped_cut(fabric_size: int, cuts: []) -> set:
    fabric = build_fabric(fabric_size)
    results = set()
    overlaped = set()
   
    for index, elf_id in cuts_to_indexes(fabric_size, parse_lines(cuts)):
        field = fabric[index]
        fabric[index] = elf_id

        if field > 0:
            overlaped.add(field)
            overlaped.add(elf_id)

            if field in results:
                results.remove(field)
            if elf_id in results:
                results.remove(elf_id)
        else:
            if not elf_id in overlaped:
                results.add(elf_id)

    return results


test_input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
assert count_overlaps_for_fabric_by_cuts(8, test_input) == 4

result = find_non_overlaped_cut(8, test_input)
assert list(result) == [3]

print("Solution for first part:", count_overlaps_for_fabric_by_cuts(1000, file_to_input_list('input.03.txt')))
print("Solution for second part:", find_non_overlaped_cut(1000, file_to_input_list('input.03.txt')))
