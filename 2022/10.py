"""
--- 2022 --- Day 10: Cathode-Ray Tube ---
"""


EXAMPLES1 = (
    ('10-exemple1.txt', 13140),
)

EXAMPLES2 = (
    ('10-exemple1.txt', None),
)

INPUT = '10.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            x, *y = line.strip().split()
            if not y:
                data.append((x, 0))
            else:
                data.append((x, int(y[0])))
    return data


def code1(data):
    target = (20, 60, 100, 140, 180, 220)
    X = 1
    cycles = 0
    strength = 0
    for op, val in data:
        if op == 'noop':
            cycles += 1
            if cycles in target:
                strength += cycles * X
        elif op == 'addx':
            cycles += 1
            if cycles in target:
                strength += cycles * X
            cycles += 1
            if cycles in target:
                strength += cycles * X
            X += val

    return strength


def code2(data):
    X = 1
    cycles = 0
    CRT = [['.' for _ in range(40)] for _ in range(6)]

    for op, val in data:
        if op == 'noop':
            cycles += 1
            i, j = divmod(cycles - 1, 40)
            if j == X - 1 or j == X or j == X + 1:
                CRT[i][j] = '#'
        elif op == 'addx':
            cycles += 1
            i, j = divmod(cycles - 1, 40)
            if j == X - 1 or j == X or j == X + 1:
                CRT[i][j] = '#'
            cycles += 1
            i, j = divmod(cycles - 1, 40)
            if j == X - 1 or j == X or j == X + 1:
                CRT[i][j] = '#'
            X += val

    for line in CRT:
        print(''.join(line))
    print()

    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
