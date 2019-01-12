def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield int(line)


def run_list_indefinitely(frequencies_list):
    while True:
        for frequency in frequencies_list:
            yield frequency


def run_up_to_first_twice(frequencies_list):
    current_frequency = 0
    results = set([current_frequency])

    for frequency in run_list_indefinitely(frequencies_list):
        current_frequency += frequency
        if current_frequency in results:
            return current_frequency
        else:
            results.add(current_frequency)


def unit_test(frequencies_list, expected_result):
    result = run_up_to_first_twice(frequencies_list)

    assert result == expected_result, f"Excepted {expected_result}, recived: {result}"


print("Solution for first part:", sum(load_input_file('input.1.txt')))

unit_test([+1, -1], 0)
unit_test([+3, +3, +4, -2, -4], 10)
unit_test([-6, +3, +8, +5, -6], 5)
unit_test([+7, +7, -2, -7, -4], 14)

temp_list = [l for l in load_input_file('input.1.txt')]
print("Solution for second part:", run_up_to_first_twice(temp_list))
