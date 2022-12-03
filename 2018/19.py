"""
--- 2018 --- Day 19: Go With The Flow ---
"""


EXAMPLES1 = (
    ('19-exemple1.txt', 6),
)

EXAMPLES2 = (
)

INPUT = '19.txt'


def read_data(filename):
    """
    Return list with pointer register then instructions
    """
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]

    program = []
    pointer_register = int(lines[0].split()[1])
    program.append(pointer_register)

    for line in lines[1:]:
        op, *args = line.strip().split()
        program.append([globals()[op]] + [int(_) for _ in args])

    return program


def addr(registers, r1, r2, r3):
    registers[r3] = registers[r1] + registers[r2]


def addi(registers, r1, x, r3):
    registers[r3] = registers[r1] + x


def mulr(registers, r1, r2, r3):
    registers[r3] = registers[r1] * registers[r2]


def muli(registers, r1, x, r3):
    registers[r3] = registers[r1] * x


def banr(registers, r1, r2, r3):
    registers[r3] = registers[r1] & registers[r2]


def bani(registers, r1, x, r3):
    registers[r3] = registers[r1] & x


def borr(registers, r1, r2, r3):
    registers[r3] = registers[r1] | registers[r2]


def bori(registers, r1, x, r3):
    registers[r3] = registers[r1] | x


def setr(registers, r1, _, r3):
    registers[r3] = registers[r1]


def seti(registers, x, _, r3):
    registers[r3] = x


def gtir(registers, x, r2, r3):
    registers[r3] = 1 if (x > registers[r2]) else 0


def gtri(registers, r1, x, r3):
    registers[r3] = 1 if (registers[r1] > x) else 0


def gtrr(registers, r1, r2, r3):
    registers[r3] = 1 if (registers[r1] > registers[r2]) else 0


def eqir(registers, x, r2, r3):
    registers[r3] = 1 if (x == registers[r2]) else 0


def eqri(registers, r1, x, r3):
    registers[r3] = 1 if (registers[r1] == x) else 0


def eqrr(registers, r1, r2, r3):
    registers[r3] = 1 if (registers[r1] == registers[r2]) else 0


def run_code(registers, program):
    pointer_register = program[0]
    program = program[1:]
    pointer = 0
    while 0 <= pointer < len(program):
        registers[pointer_register] = pointer
        opcode, *args = program[pointer]
        # print(pointer, opcode.__name__, *args, registers)
        back = registers[0]
        opcode(registers, *args)
        # if registers[0] != back:
            # print(pointer, opcode.__name__, *args, registers)
        pointer = registers[pointer_register]
        pointer += 1


def code1(program):
    registers = [0] * 6
    run_code(registers, program)
    return registers[0]


def code2(program):
    registers = [0] * 6
    registers[0] = 1
    run_code(registers, program)
    return registers[0]


def sum_of_divisors(n):
    count = 0
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            count += i
    count += n
    return count


def code2(_):
    # Obtained by looking at logs when r0 changes. For instance with r0 = 0, it
    # goes :
    # 7 addr 1 0 0 [1, 1, 898, 898, 7, 1]
    # 7 addr 1 0 0 [3, 2, 898, 449, 7, 1]
    # 7 addr 1 0 0 [452, 449, 898, 2, 7, 1]
    # 7 addr 1 0 0 [1350, 898, 898, 1, 7, 1]
    # r2 is constant and is the argument and is 10551298 with r0 = 1 when starting.
    return sum_of_divisors(10551298)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
