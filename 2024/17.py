"""
--- Day 17: Chronospatial Computer ---
"""


import re


EXAMPLES1 = (
    ('17-exemple1.txt', '4,6,3,5,6,3,5,2,1,0'),
)

EXAMPLES2 = (
)

INPUT = '17.txt'


def read_data(filename):
    registers = {}
    with open(filename) as f:
        for line in f.readlines():
            if match := re.match(r'Register ([ABC]): (\d+)', line):
                registers[match[1]] = int(match[2])
            else:
                program = [int(_) for _ in re.findall(r'(\d+)', line)]
    return registers, program


def combovalue(registers, x):
    if 0 <= x <= 3:
        return x
    elif x <= 6:
        return registers['....ABC'[x]]
    else:
        assert 0


def run(registers, program):
    pointer = 0
    output = []
    while pointer < len(program):
        instruction = program[pointer]
        operand = program[pointer + 1]

        match instruction:
            case 0: # adv
                registers['A'] = registers['A'] // (2 ** combovalue(registers, operand))
                pointer += 2
            case 1: # bxl
                registers['B'] = registers['B'] ^ operand
                pointer += 2
            case 2: # bst
                registers['B'] = combovalue(registers, operand) % 8
                pointer += 2
            case 3: # jnz
                if registers['A'] == 0:
                    pointer += 2
                else:
                    pointer = operand
            case 4: # bxc
                registers['B'] = registers['B'] ^ registers['C']
                pointer += 2
            case 5: # out
                output.append(combovalue(registers, operand) % 8)
                pointer += 2
            case 6: # bdv
                registers['B'] = registers['A'] // (2 ** combovalue(registers, operand))
                pointer += 2
            case 7: # cdv
                registers['C'] = registers['A'] // (2 ** combovalue(registers, operand))
                pointer += 2
    return output


def myprog(A):
    # direct transcription
    out = []
    while A:
        B = A % 8
        B = B ^ 2
        C = A // (2 ** B)
        B = B ^ C
        B = B ^ 7
        out.append(B % 8)
        A = A // 8
    return out


def myprog2(A):
    out = []
    while A:
        A2 = A & 1023       # output depends only on 10 last bits of A
        B = (A2 % 8) ^ 2
        C = (A2 >> B) % 8
        B = B ^ C
        B = B ^ 7
        out.append(B)
        A = A // 8
    return out


OUTPUT = [5, 4, 5, 7, 1, 0, 3, 2, 7, 5, 5, 3, 1, 0, 3, 2, 1, 6, 5, 7, 1, 0, 2, 2, 3, 7, 5, 3, 1, 0, 2, 2, 5, 0, 5, 7, 1, 0, 1, 3, 7, 1, 5, 3, 1, 0, 1, 3, 1, 2, 5, 7, 1, 0, 0, 3, 3, 3, 5, 3, 1, 0, 0, 3, 5, 4, 5, 7, 0, 0, 7, 0, 7, 5, 5, 3, 0, 0, 7, 0, 1, 6, 5, 7, 0, 0, 6, 0, 3, 7, 5, 3, 0, 0, 6, 0, 5, 0, 5, 7, 0, 0, 5, 1, 7, 1, 5, 3, 0, 0, 5, 1, 1, 2, 5, 7, 0, 0, 4, 1, 3, 3, 5, 3, 0, 0, 4, 1, 5, 4, 5, 7, 3, 1, 3, 6, 7, 5, 5, 3, 3, 1, 3, 6, 1, 6, 5, 7, 3, 1, 2, 6, 3, 7, 5, 3, 3, 1, 2, 6, 5, 0, 5, 7, 3, 1, 1, 7, 7, 1, 5, 3, 3, 1, 1, 7, 1, 2, 5, 7, 3, 1, 0, 7, 3, 3, 5, 3, 3, 1, 0, 7, 5, 4, 5, 7, 2, 1, 7, 4, 7, 5, 5, 3, 2, 1, 7, 4, 1, 6, 5, 7, 2, 1, 6, 4, 3, 7, 5, 3, 2, 1, 6, 4, 5, 0, 5, 7, 2, 1, 5, 5, 7, 1, 5, 3, 2, 1, 5, 5, 1, 2, 5, 7, 2, 1, 4, 5, 3, 3, 5, 3, 2, 1, 4, 5, 5, 4, 5, 7, 5, 2, 3, 2, 7, 5, 5, 3, 5, 2, 3, 2, 1, 6, 5, 7, 5, 2, 2, 2, 3, 7, 5, 3, 5, 2, 2, 2, 5, 0, 5, 7, 5, 2, 1, 3, 7, 1, 5, 3, 5, 2, 1, 3, 1, 2, 5, 7, 5, 2, 0, 3, 3, 3, 5, 3, 5, 2, 0, 3, 5, 4, 5, 7, 4, 2, 7, 0, 7, 5, 5, 3, 4, 2, 7, 0, 1, 6, 5, 7, 4, 2, 6, 0, 3, 7, 5, 3, 4, 2, 6, 0, 5, 0, 5, 7, 4, 2, 5, 1, 7, 1, 5, 3, 4, 2, 5, 1, 1, 2, 5, 7, 4, 2, 4, 1, 3, 3, 5, 3, 4, 2, 4, 1, 5, 4, 5, 7, 7, 3, 3, 6, 7, 5, 5, 3, 7, 3, 3, 6, 1, 6, 5, 7, 7, 3, 2, 6, 3, 7, 5, 3, 7, 3, 2, 6, 5, 0, 5, 7, 7, 3, 1, 7, 7, 1, 5, 3, 7, 3, 1, 7, 1, 2, 5, 7, 7, 3, 0, 7, 3, 3, 5, 3, 7, 3, 0, 7, 5, 4, 5, 7, 6, 3, 7, 4, 7, 5, 5, 3, 6, 3, 7, 4, 1, 6, 5, 7, 6, 3, 6, 4, 3, 7, 5, 3, 6, 3, 6, 4, 5, 0, 5, 7, 6, 3, 5, 5, 7, 1, 5, 3, 6, 3, 5, 5, 1, 2, 5, 7, 6, 3, 4, 5, 3, 3, 5, 3, 6, 3, 4, 5, 5, 4, 5, 7, 1, 4, 3, 2, 7, 5, 5, 3, 1, 4, 3, 2, 1, 6, 5, 7, 1, 4, 2, 2, 3, 7, 5, 3, 1, 4, 2, 2, 5, 0, 5, 7, 1, 4, 1, 3, 7, 1, 5, 3, 1, 4, 1, 3, 1, 2, 5, 7, 1, 4, 0, 3, 3, 3, 5, 3, 1, 4, 0, 3, 5, 4, 5, 7, 0, 4, 7, 0, 7, 5, 5, 3, 0, 4, 7, 0, 1, 6, 5, 7, 0, 4, 6, 0, 3, 7, 5, 3, 0, 4, 6, 0, 5, 0, 5, 7, 0, 4, 5, 1, 7, 1, 5, 3, 0, 4, 5, 1, 1, 2, 5, 7, 0, 4, 4, 1, 3, 3, 5, 3, 0, 4, 4, 1, 5, 4, 5, 7, 3, 5, 3, 6, 7, 5, 5, 3, 3, 5, 3, 6, 1, 6, 5, 7, 3, 5, 2, 6, 3, 7, 5, 3, 3, 5, 2, 6, 5, 0, 5, 7, 3, 5, 1, 7, 7, 1, 5, 3, 3, 5, 1, 7, 1, 2, 5, 7, 3, 5, 0, 7, 3, 3, 5, 3, 3, 5, 0, 7, 5, 4, 5, 7, 2, 5, 7, 4, 7, 5, 5, 3, 2, 5, 7, 4, 1, 6, 5, 7, 2, 5, 6, 4, 3, 7, 5, 3, 2, 5, 6, 4, 5, 0, 5, 7, 2, 5, 5, 5, 7, 1, 5, 3, 2, 5, 5, 5, 1, 2, 5, 7, 2, 5, 4, 5, 3, 3, 5, 3, 2, 5, 4, 5, 5, 4, 5, 7, 5, 6, 3, 2, 7, 5, 5, 3, 5, 6, 3, 2, 1, 6, 5, 7, 5, 6, 2, 2, 3, 7, 5, 3, 5, 6, 2, 2, 5, 0, 5, 7, 5, 6, 1, 3, 7, 1, 5, 3, 5, 6, 1, 3, 1, 2, 5, 7, 5, 6, 0, 3, 3, 3, 5, 3, 5, 6, 0, 3, 5, 4, 5, 7, 4, 6, 7, 0, 7, 5, 5, 3, 4, 6, 7, 0, 1, 6, 5, 7, 4, 6, 6, 0, 3, 7, 5, 3, 4, 6, 6, 0, 5, 0, 5, 7, 4, 6, 5, 1, 7, 1, 5, 3, 4, 6, 5, 1, 1, 2, 5, 7, 4, 6, 4, 1, 3, 3, 5, 3, 4, 6, 4, 1, 5, 4, 5, 7, 7, 7, 3, 6, 7, 5, 5, 3, 7, 7, 3, 6, 1, 6, 5, 7, 7, 7, 2, 6, 3, 7, 5, 3, 7, 7, 2, 6, 5, 0, 5, 7, 7, 7, 1, 7, 7, 1, 5, 3, 7, 7, 1, 7, 1, 2, 5, 7, 7, 7, 0, 7, 3, 3, 5, 3, 7, 7, 0, 7, 5, 4, 5, 7, 6, 7, 7, 4, 7, 5, 5, 3, 6, 7, 7, 4, 1, 6, 5, 7, 6, 7, 6, 4, 3, 7, 5, 3, 6, 7, 6, 4, 5, 0, 5, 7, 6, 7, 5, 5, 7, 1, 5, 3, 6, 7, 5, 5, 1, 2, 5, 7, 6, 7, 4, 5, 3, 3, 5, 3, 6, 7, 4, 5]


def myprog3(A):
    out = []
    while A:
        out.append(OUTPUT[A & 1023])
        A = A // 8
    return out


def reverse_program(program):
    stack = []
    rang = 0
    for index, digit in enumerate(OUTPUT):
        if digit == program[rang]:
            binary = ('0' * 16 + bin(index)[2:])[-10:]
            stack.append((rang + 1, binary[:7], binary[7:]))

    while stack:
        rang, amorce, lowerbits = stack.pop()
        if rang == len(program):
            yield int(amorce + lowerbits, 2)
        else:
            for index, digit in enumerate(OUTPUT):
                if digit == program[rang]:
                    binary = ('0' * 16 + bin(index)[2:])[-10:]
                    if binary[-7:] == amorce:
                        stack.append((rang + 1, binary[:7], binary[7:] + lowerbits))


def gen_output():
    out = []
    for n in range(1024):
        B = (n % 8) ^ 2
        C = (n >> B) % 8
        B = B ^ C
        B = B ^ 7
        out.append(B)
    print(out)


def code1(data):
    registers, program = data
    return ','.join([str(_) for _ in run(registers, program)])


def code2(data):
    _, program = data
    x = sorted(reverse_program(program))
    print('Check', myprog(x[0]), myprog(x[0]) == program)
    return x[0]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
