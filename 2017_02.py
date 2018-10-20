input_array = [
    # '\t+' -> ', '
    # '^' -> '['
    # '$' -> '],'
]

result = sum([max(row) - min(row) for row in input_array])

print(result)
