"""
--- 2015 --- Day 23: Opening the Turing Lock ---
"""


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '23.txt'


def read_data(filename):
    instructions = []
    with open(filename) as f:
        for line in [line.strip() for line in f.readlines()]:
            op, *args = line.replace(',', '').split()
            if op in ('hlf', 'tpl', 'inc'):
                instructions.append((op, args[0]))
            elif op == 'jmp':
                instructions.append((op, int(args[0])))
            else:
                instructions.append((op, args[0], int(args[1])))
    return instructions


def run(instructions, registers):
    pointer = 0
    while True:
        if pointer < 0 or pointer >= len(instructions):
            break
        op, arg1, *arg2 = instructions[pointer]
        if op == 'hlf':
            registers[arg1] //= 2
            pointer += 1
        elif op == 'tpl':
            registers[arg1] *= 3
            pointer += 1
        elif op == 'inc':
            registers[arg1] += 1
            pointer += 1
        elif op == 'jmp':
            pointer += arg1
        elif op == 'jie':
            if registers[arg1] % 2 == 0:
                pointer += arg2[0]
            else:
                pointer += 1
        elif op == 'jio':
            if registers[arg1] == 1:
                pointer += arg2[0]
            else:
                pointer += 1
        else:
            assert 0
    return registers['b']


def code1(instructions):
    registers = {'a': 0, 'b': 0}
    return run(instructions, registers)

def code2(instructions):
    registers = {'a': 1, 'b': 0}
    return run(instructions, registers)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
