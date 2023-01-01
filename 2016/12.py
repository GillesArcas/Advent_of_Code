"""
--- 2016 --- Day 12: Leonardo's Monorail ---
"""


EXAMPLES1 = (
    ('12-exemple1.txt', 42),
)

EXAMPLES2 = (
)

INPUT = '12.txt'


def value(x):
    try:
        return int(x)
    except:
        return x


def read_data(filename):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]
    instructions = []
    for line in lines:
        instructions.append([value(_) for _ in line.split()])
    return instructions


def run(instructions, registers):
    pointer = 0
    while pointer < len(instructions):
        op, *args = instructions[pointer]
        if op == 'cpy':
            if isinstance(args[0], int):
                registers[args[1]] = args[0]
            else:
                registers[args[1]] = registers[args[0]]
            pointer += 1
        elif op == 'inc':
            registers[args[0]] += 1
            pointer += 1
        elif op == 'dec':
            registers[args[0]] -= 1
            pointer += 1
        elif op == 'jnz':
            if isinstance(args[0], int):
                cond = args[0]
            else:
                cond = registers[args[0]]
            if cond == 0:
                pointer += 1
            else:
                pointer += args[1]
    return registers['a']


def code1(instructions):
    registers = dict(a=0, b=0, c=0, d=0)
    return run(instructions, registers)


def code2(instructions):
    registers = dict(a=0, b=0, c=1, d=0)
    return run(instructions, registers)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
