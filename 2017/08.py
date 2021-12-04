import re

from collections import defaultdict


EXAMPLES1 = (
    ('08-exemple1.txt', 1),
)

EXAMPLES2 = (
    ('08-exemple1.txt', 10),
)

INPUT =  '08-input.txt'


def read_data(fn):
    # njb inc 981 if dou <= 5159

    registers = set()
    instructions = list()
    with open(fn) as f:
        for line in f:
            register, incdec, incr, _, regtest, logop, const = line.strip().split()
            registers.add(register)
            registers.add(regtest)
            instructions.append((register, incdec, int(incr), regtest, logop, int(const)))

    return registers, instructions


def applylogop(regtest, logop, const):
    if logop == '<':
        return regtest < const
    if logop == '>':
        return regtest > const
    if logop == '<=':
        return regtest <= const
    if logop == '>=':
        return regtest >= const
    if logop == '==':
        return regtest == const
    if logop == '!=':
        return regtest != const


def code(args):
    registers, instructions = args
    regvalues = defaultdict(int)
    allmax = 0
    for register, incdec, incr, regtest, logop, const in instructions:
        if applylogop(regvalues[regtest], logop, const):
            if incdec == 'dec':
                incr = -incr
            regvalues[register] += incr
            if regvalues[register] > allmax:
                allmax = regvalues[register]
    return max(regvalues.values()), allmax


def code1(args):
     return code(args)[0]


def code2(args):
    return code(args)[1]


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
