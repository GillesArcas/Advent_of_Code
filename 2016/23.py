"""
--- 2016 --- Day 23: Safe Cracking ---
"""


EXAMPLES1 = (
    ('23-exemple1.txt', 3),
)

EXAMPLES2 = (
)

INPUT = '23.txt'


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


def argvalue(registers, x):
    if isinstance(x, int):
        return x
    else:
        return registers[x]


def run(instructions, registers):
    pointer = 0
    while pointer < len(instructions):
        op, *args = instructions[pointer]
        if op == 'cpy':
            registers[args[1]] = argvalue(registers, args[0])
            pointer += 1
        elif op == 'inc':
            registers[args[0]] += 1
            pointer += 1
        elif op == 'dec':
            registers[args[0]] -= 1
            pointer += 1
        elif op == 'jnz':
            cond = argvalue(registers, args[0])
            if cond == 0:
                pointer += 1
            else:
                pointer += argvalue(registers, args[1])
        elif op == 'tgl':
            p = pointer + argvalue(registers, args[0])
            if 0 <= p < len(instructions):
                op2, *args2 = instructions[p]
                if len(args2) == 1:
                    if op2 == 'inc':
                        instructions[p][0] = 'dec'
                    else:
                        instructions[p][0] = 'inc'
                elif len(args2) == 2:
                    if op2 == 'jnz':
                        instructions[p][0] = 'cpy'
                    else:
                        instructions[p][0] = 'jnz'
            pointer += 1

    return registers['a']


def code1(instructions):
    registers = dict(a=7, b=0, c=0, d=0)
    return run(instructions, registers)


def code2(instructions):
    # 10 minutes
    registers = dict(a=12, b=0, c=0, d=0)
    return run(instructions, registers)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
