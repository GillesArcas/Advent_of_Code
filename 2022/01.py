"""
--- 2022 --- Day 1: Calorie Counting ---
"""


import re


EXAMPLES1 = (
    ('01-exemple1.txt', 24000),
)

EXAMPLES2 = (
    ('01-exemple1.txt', 45000),
)

INPUT = '01.txt'


def read_data(filename):
    with open(filename) as f:
        content = f.read()
    lists = re.findall(r'((?:\d+\n)+)', content)
    return [[int(_) for _ in onelist.splitlines()] for onelist in lists]


def code1(data):
    return max(sum(_) for _ in data)


def code2(data):
    return sum(list(sorted((sum(_) for _ in data), reverse=True))[:3])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
