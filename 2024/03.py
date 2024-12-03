"""
--- Day 3: Mull It Over ---
"""


import re


EXAMPLES1 = (
    ('03-exemple1.txt', 161),
)

EXAMPLES2 = (
    ('03-exemple2.txt', 48),
)

INPUT = '03.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read()


def code1(data):
    result = 0
    for match in re.finditer(r'mul\((\d{1,3}),(\d{1,3})\)', data):
        result += int(match[1]) * int(match[2])
    return result


def code2(data):
    result = 0
    enabled = True
    for match in re.finditer(r'(do)\(\)|(don.t)\(\)|(mul)\((\d{1,3}),(\d{1,3})\)', data):
        if match[1] == 'do':
            enabled = True
        elif match[2] == "don't":
            enabled = False
        if match[3] == 'mul' and enabled:
            result += int(match[4]) * int(match[5])
    return result


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
