def find_pair(row):
    sorted_row = sorted(row, reverse=True)

    while sorted_row:
        the_biggest = sorted_row.pop(0)
        for x in sorted_row:
            if the_biggest % x == 0:
                return (the_biggest, x)


input_array = [
    # '\t+' -> ', '
    # '^' -> '['
    # '$' -> '],'
]

# First part
result_a = sum([max(row) - min(row) for row in input_array])
print(result_a)

# Second part
pairs_table = [find_pair(row) for row in input_array]
result_b = sum([int(x / y) for x, y in pairs_table])
print(result_b)
