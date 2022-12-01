"""
--- Day 16: Chronal Classification
"""


import re


EXAMPLES1 = (
    ('16-exemple1.txt', 1),
)

EXAMPLES2 = (
)

INPUT = '16.txt'


SAMPLE_PAT = r"""Before: \[(\d+), (\d+), (\d+), (\d+)\]
(\d+) (\d+) (\d+) (\d+)
After:  \[(\d+), (\d+), (\d+), (\d+)\]
"""


def read_data(filename):
    with open(filename) as f:
        data = f.read()

    samples = []
    for sample in re.findall(SAMPLE_PAT, data):
        x = [int(_) for _ in sample]
        samples.append(tuple([tuple(x[4:8]), tuple(x[0:4]), tuple(x[8:12])]))

    match = re.search(r'\n\n\n(.*)', data, flags=re.DOTALL)
    if match is None:
        program = []
    else:
        program = []
        for instr in match.group(1).splitlines():
            program.append([int(_) for _ in instr.strip().split()])

    return samples, program


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


OPCODES = (addr, addi, mulr, muli, banr, bani, borr, bori,
           setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr)


def opcode_matchs(instr, reg_before, reg_after):
    matchs = []
    for opcode in OPCODES:
        registers = list(reg_before)
        opcode(registers, *instr[1:])
        if tuple(registers) == reg_after:
            matchs.append(opcode)
    return matchs


def code1(data):
    samples, _ = data
    count = 0
    for instr, reg_before, reg_after in samples:
        matchs = opcode_matchs(instr, reg_before, reg_after)
        if len(matchs) >= 3:
            count += 1

    return count


def run_code(registers, opcode_func, program):
    for instr in program:
        if not instr:
            continue
        code, *param = instr
        opcode_func[code](registers, *param)


def code2(data):
    samples, program = data

    # possible opcodes for functions
    possibles = {func:set() for func in OPCODES}
    for instr, reg_before, reg_after in samples:
        funcs = opcode_matchs(instr, reg_before, reg_after)
        for func in funcs:
            possibles[func].add(instr[0])

    # suppose that there is always a function with a single possible opcode when
    # a set of functions is defined
    opcode_func = [None] * 16
    while possibles:
        to_be_removed = None
        for func, opcodes in possibles.items():
            if len(opcodes) == 1:
                to_be_removed = func
                opcode = list(opcodes)[0]
                opcode_func[opcode] = func
                for opcodes2 in possibles.values():
                    opcodes2.discard(opcode)
                break
        possibles.pop(to_be_removed, None)

    for code, f in enumerate(opcode_func):
        print(code, f.__name__)

    registers = [0] * 4
    run_code(registers, opcode_func, program)

    return registers[0]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
