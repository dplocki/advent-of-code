import hashlib
import multiprocessing


def load_input_file(file_name: str):
    with open(file_name) as file:
        return file.read()


def generate_hashes(key: str, start_index: int, loop_index):
    index = start_index
    while True:
        yield index, hashlib.md5((key + str(index)).encode()).hexdigest()
        index += loop_index


def find_index_starts_with(hash_generator, starts_with: str, result: multiprocessing.Queue):
    for index, hash in hash_generator:
        if hash.startswith(starts_with):
            result.put(index)


def worker(key: str, starts_with: str, start_index: int, loop_index: int, result: multiprocessing.Queue):
    generator = generate_hashes(key, start_index, loop_index)
    find_index_starts_with(generator, starts_with, result)


def find_the_lowest_index(key: str, how_many_zeros_on_begin: int):
    cpu_count = multiprocessing.cpu_count()
    answer = multiprocessing.Queue()
    check = '0' * how_many_zeros_on_begin

    jobs = [
        multiprocessing.Process(target=worker, args=(
            key,
            check,
            cpu_index,
            cpu_count,
            answer)
        )
        for cpu_index in range(cpu_count)
    ]

    for j in jobs:
        j.start()

    result = answer.get()

    for j in jobs:
        j.terminate()

    return result


# The solution is taken from: https://adventofcode.com/2015/day/4/input
key = load_input_file('input.04.txt')

print("Solution for the first part:", find_the_lowest_index(key, 5))

# The solution for it is not deterministic, but I decided to leave it anyway:
# It is my first Advent task in which I used the concurrent programming
print("Solution for the second part:", find_the_lowest_index(key, 6))
