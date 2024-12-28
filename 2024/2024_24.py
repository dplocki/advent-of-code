from typing import Dict, Iterable, Tuple


def load_input_file(file_name: str) -> str:
    with open(file_name) as file:
        return file.read().rstrip()


def parse(task_input: Iterable[str]) -> Tuple[Dict[str, int], Dict[str, Tuple[str, str, str]]]:
    raw_init_vales, raw_gates = task_input.split('\n\n')

    gates_outputs = {
        tokens[0]: int(tokens[1])
        for tokens in map(lambda line: line.split(': '), raw_init_vales.splitlines())}

    instructions = {
        out_gate: (operation, left_gate, right_gate)
        for left_gate, operation, right_gate, _, out_gate in map(lambda line: line.split(' '), raw_gates.splitlines())}

    return gates_outputs, instructions


def get_gate_output(gates_outputs: Dict[str, int], instructions: Dict[str, Tuple[str, str, str]], gate: str) -> int:
    if gate not in gates_outputs or gates_outputs[gate] == None:
        instruction = instructions[gate]

        if instruction[0] == 'AND':
            value = get_gate_output(gates_outputs, instructions, instruction[1]) and \
                    get_gate_output(gates_outputs, instructions, instruction[2])
        elif instruction[0] == 'OR':
            value = get_gate_output(gates_outputs, instructions, instruction[1]) or \
                    get_gate_output(gates_outputs, instructions, instruction[2])
            gates_outputs[gate] = int(value)
        elif instruction[0] == 'XOR':
            value = get_gate_output(gates_outputs, instructions, instruction[1]) != \
                    get_gate_output(gates_outputs, instructions, instruction[2])

        gates_outputs[gate] = int(value)

    return gates_outputs[gate]


def solution_for_first_part(task_input: Iterable[str]) -> int:
    gates_schema, instructions = parse(task_input)

    return int(''.join(
        str(get_gate_output(gates_schema, instructions, z_gate))
        for z_gate in sorted((k for k in instructions.keys() if k.startswith('z')), reverse=True)), 2)


example_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

assert solution_for_first_part(example_input) == 2024

# The input is taken from: https://adventofcode.com/2024/day/24/input
task_input = load_input_file('input.24.txt')
print("Solution for the first part:", solution_for_first_part(task_input))


FIXES = [
    # add pairs to be replaced:
    #
    # (which_gate, which_gate),
    # (which_gate, which_gate),
    # (which_gate, which_gate),
    # (which_gate, which_gate),
]


def apply_fixes(instructions: Dict[str, Tuple[str, str, str]]) -> Dict[str, Tuple[str, str, str]]:
    for a, b in FIXES:
        instructions[a], instructions[b] = instructions[b], instructions[a]

    return instructions


def get_gates_for(instructions: Dict[str, Tuple[str, str, str]], gate_prefix: str) -> Iterable[str]:
    return sorted(k for k in instructions.keys() if k.startswith(gate_prefix))


def run_test(task_input: Iterable[str]) -> None:
    gates_schema, instructions = parse(task_input)

    apply_fixes(instructions)

    new_gates_schema = {
        key: 0
        for key in gates_schema
    }

    for gate in get_gates_for(gates_schema, 'x'):
        new_gates_schema[gate] = 1

    for gate in get_gates_for(instructions, 'z'):
        print(gate, new_gates_schema.get(gate.replace('z', 'x'), ' '), new_gates_schema.get(gate.replace('z', 'y'), ' '), get_gate_output(new_gates_schema, instructions, gate))


def get_instructions_using_gate(instructions: Dict[str, Tuple[str, str, str]], gate: str) -> Dict[str, Tuple[str, str, str]]:
    return {
            k: instruction
            for k, instruction in instructions.items()
            if gate in instruction
        }


def print_gates_per_bit(task_input: Iterable[str]) -> None:
    _, instructions = parse(task_input)

    apply_fixes(instructions)

    print('z00')
    print('\t', 'z00', '=>', instructions['z00'], 'out')
    for k, v in get_instructions_using_gate(instructions, 'x00').items():
        if k != 'z00':
            print('\t', k, '=>', v, 'out_carry')
            carry = k

    for bit_index in range(1, 45):

        number = str(bit_index).zfill(2)
        x_gate = 'x' + number
        z_gate = 'z' + number
        temp_gate = None

        print(z_gate)
        for k, v in get_instructions_using_gate(instructions, x_gate).items():
            if 'XOR' in v:
                print('\t', k, '=>', v, 'partial_sum')
            elif 'AND' in v:
                print('\t', k, '=>', v, 'carry1')

        for k, v in get_instructions_using_gate(instructions, carry).items():
            if 'AND' in v:
                print('\t', k, '=>', v, 'carry2')
                temp_gate = k

        for k, v in get_instructions_using_gate(instructions, temp_gate).items():
            if 'OR' in v:
                print('\t', k, '=>', v, 'out_carry')
                carry = k

        print('\t', z_gate, '=>', instructions[z_gate], 'out')



def solution_for_second_part(task_input: Iterable[str]) -> int:
    return ','.join(sorted(wire for fix in FIXES for wire in fix))

    run_test(task_input)
    print_gates_per_bit(task_input)


print("Solution for the second part:", solution_for_second_part(task_input))
