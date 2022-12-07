"""
--- 2018 --- Day 21: Chronal Conversion ---
"""


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '21.txt'


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


def run_code(registers, program, goal):
    sol = set()
    pointer_register = program[0]
    program = program[1:]
    pointer = 0
    while 0 <= pointer < len(program):
        if pointer == 28:
            if goal == code1:
                return registers[4]
            else:
                print(registers[4])
                if registers[4] in sol:
                    return prev
                else:
                    prev = registers[4]
                    sol.add(registers[4])
        registers[pointer_register] = pointer
        opcode, *args = program[pointer]
        opcode(registers, *args)
        pointer = registers[pointer_register]
        pointer += 1


def code1(program):
    registers = [0] * 6
    return run_code(registers, program, code1)


def code2(program):
    # some help from reddit to understand the question
    registers = [0] * 6
    return run_code(registers, program, code2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
