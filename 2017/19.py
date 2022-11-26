import re


EXAMPLES1 = (
    ('19-exemple1.txt', 'ABCDEF'),
)

EXAMPLES2 = (
    ('19-exemple1.txt', 38),
)

INPUT = '19.txt'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def read_data(data):
    with open(data) as f:
        diagram = f.readlines()
        # add empty line to avoid testing limits (suppose this not necessary
        # in other directions)
        diagram.append(' ' * len(diagram[0]))
        return diagram


def follow(diagram):
    i = 0
    j = diagram[0].index('|')
    d = 'S'
    path = ''
    steps = 0
    while True:
        current = diagram[i][j]
        if current == ' ':
            return path, steps
        steps += 1
        if current in LETTERS:
            path += current
        if (current in '|-' or current in LETTERS) and d == 'S':
            i += 1
        elif (current in '|-' or current in LETTERS) and d == 'N':
            i -= 1
        elif (current in '|-' or current in LETTERS) and d == 'E':
            j += 1
        elif (current in '|-' or current in LETTERS) and d == 'W':
            j -= 1
        elif current == '+':
            if d in 'SN':
                j, d = (j - 1, 'W') if diagram[i][j - 1] in '-' + LETTERS else (j + 1, 'E')
            else:
                i, d = (i - 1, 'N') if diagram[i - 1][j] in '|' + LETTERS else (i + 1, 'S')


def code1(data):
    trace, _ = follow(data)
    return trace


def code2(data):
    _, steps = follow(data)
    return steps


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
