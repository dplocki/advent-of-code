import hashlib


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def find_hash_with_5zeros(door_id: str):
    i = 0
    while True: 
        md5 = hashlib.md5()
        md5.update(door_id.encode('utf-8'))
        md5.update(str(i).encode('utf-8'))
        md5_hash = md5.hexdigest()

        if md5_hash[:5] == '00000':
            yield md5_hash[5]

        i += 1


def find_password(input: str) -> str:
    return ''.join(
            map(
                lambda x: x[0],
                zip(
                    find_hash_with_5zeros(input),
                    range(8)
                )
            )
        )


assert find_password('abc') == '18f47a30'

# The input is taken from: https://adventofcode.com/2016/day/5/input
input = load_input_file('input.05.txt')
print("Solution for the first part:", find_password(input))
