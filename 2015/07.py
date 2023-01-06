"""
--- 2015 --- Day 7: Some Assembly Required ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '07.txt'


def read_data(filename):
    instructions = []
    with open(filename) as f:
        for line in (_.strip() for _ in f.readlines()):
            if match := re.match(r'([a-z0-9]+) (AND|OR|LSHIFT|RSHIFT) ([a-z0-9]+) -> ([a-z]+)', line):
                instruction = list(match.group(2, 1, 3, 4))
                if instruction[1].isdigit():
                    instruction[1] = int(instruction[1])
                if instruction[2].isdigit():
                    instruction[2] = int(instruction[2])
            elif match := re.match(r'NOT ([a-z]+) -> ([a-z]+)', line):
                instruction = ['NOT'] + list(match.group(1, 2))
            elif match := re.match(r'([a-z0-9]+) -> ([a-z]+)', line):
                instruction = ['SET', match.group(1), match.group(2)]
                if instruction[1].isdigit():
                    instruction[1] = int(instruction[1])
            else:
                assert 0, line
            # print(instruction)
            instructions.append(instruction)
    return instructions


def argvalue(arg, wires):
    if isinstance(arg, int):
        return arg
    elif arg in wires:
        return wires[arg]
    else:
        return None


def apply(instruction, wires):
    op, *args, dest = instruction
    values = [argvalue(_, wires) for _ in args]
    if any(_ is None for _ in values):
        return False
    else:
        if op == 'SET':
            wires[dest] = values[0]
        elif op == 'NOT':
            wires[dest] = (~values[0]) & 65535
        elif op == 'AND':
            wires[dest] = values[0] & values[1]
        elif op == 'OR':
            wires[dest] = values[0] | values[1]
        elif op == 'RSHIFT':
            wires[dest] = values[0] >> values[1]
        elif op == 'LSHIFT':
            wires[dest] = (values[0] << values[1]) & 65535
        return True


def code1(instructions):
    available = [True for instruction in instructions]
    wires = {}
    while any(available):
        for index, instruction in enumerate(instructions):
            if available[index] and apply(instruction, wires):
                available[index] = False

    return wires['a']


def code2(instructions):
    val_a = code1(instructions)
    for instruction in instructions:
        if instruction[0] == 'SET' and instruction[-1] == 'b':
            instruction[1] = val_a
            break
    return code1(instructions)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
