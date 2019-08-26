import hashlib


SHOW_CINEMATIC_DECRIPTION_ANIMATION = False


def load_input_file(file_name):
    with open(file_name) as file:
        return file.read().strip()


def find_hash_with_five_zeros(door_id: str):
    i = 0
    while True: 
        md5 = hashlib.md5()
        md5.update(door_id.encode('utf-8'))
        md5.update(str(i).encode('utf-8'))
        md5_hash = md5.hexdigest()

        if md5_hash[:5] == '00000':
            yield md5_hash[5], md5_hash[6]

        i += 1


def solution_for_first_part(door_id: str) -> str:
    return ''.join(
            map(
                lambda x: x[0][0],
                zip(
                    find_hash_with_five_zeros(door_id),
                    range(8)
                )
            )
        )


def solution_for_second_part(door_id: str, show_steps = False) -> str:
    
    def get_only_eight_characters(door_id):
        PASSWORD_LENGTH = 8
        EMPTY_CHARACTER = '_'
        result = [EMPTY_CHARACTER] * PASSWORD_LENGTH

        generator = find_hash_with_five_zeros(door_id)
        while EMPTY_CHARACTER in result:
            position_character, character = next(generator)
            if not position_character in '01234567':
                continue

            position = int(position_character)
            if result[position] != EMPTY_CHARACTER:
                continue

            result[position] = character
            if show_steps:
                print(result)

        return result

    return ''.join(get_only_eight_characters(door_id))


assert solution_for_first_part('abc') == '18f47a30'
assert solution_for_second_part('abc')  == '05ace8e3'

# The input is taken from: https://adventofcode.com/2016/day/5/input
input = load_input_file('input.05.txt')
print("Solution for the first part:", solution_for_first_part(input))
print("Solution for the second part:", solution_for_second_part(input, SHOW_CINEMATIC_DECRIPTION_ANIMATION))
