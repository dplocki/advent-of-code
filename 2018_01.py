def load_input_file(file_name):
    with open(file_name) as file:
        for line in file:
            yield int(line)


result = sum(load_input_file('input.1.txt'))

print("Solution for first part:", result)
