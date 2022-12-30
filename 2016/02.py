"""
--- 2016 --- Day 2: Bathroom Security ---
"""


EXAMPLES1 = (
    ('02-exemple1.txt', '1985'),
)

EXAMPLES2 = (
    ('02-exemple1.txt', '5DB3'),
)

INPUT = '02.txt'


def read_data(filename):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]
    return data


KEYBOARD1 = ('123', '456', '789')
KEYBOARD2 = (
    '  1  ',
    ' 234 ',
    '56789',
    ' ABC ',
    '  D  ')


def move(x, y, instruction, maxi):
    if instruction == 'U':
        if y == 0:
            return None
        else:
            return x, y - 1
    elif instruction == 'D':
        if y == maxi:
            return None
        else:
            return x, y + 1
    elif instruction == 'L':
        if x == 0:
            return None
        else:
            return x - 1, y
    elif instruction == 'R':
        if x == maxi:
            return None
        else:
            return x + 1, y


def code1(lines):
    code = []
    x, y = 1, 1
    for line in lines:
        for instruction in line:
            ret = move(x, y, instruction, 2)
            if ret:
                x, y = ret
        code.append(KEYBOARD1[y][x])
    return ''.join(code)


def code2(lines):
    code = []
    x, y = 0, 2
    for line in lines:
        for instruction in line:
            ret = move(x, y, instruction, 4)
            if ret and KEYBOARD2[ret[1]][ret[0]] != ' ':
                x, y = ret
        code.append(KEYBOARD2[y][x])
    return ''.join(code)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
