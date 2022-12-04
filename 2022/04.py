"""
--- 2022 --- Day 4: Camp Cleanup ---
"""


import re


EXAMPLES1 = (
    ('04-exemple1.txt', 2),
)

EXAMPLES2 = (
    ('04-exemple1.txt', 4),
)

INPUT = '04.txt'


def read_data(filename):
    data = []
    with open(filename) as f:
        for line in [_.strip() for _ in f.readlines()]:
            data.append(tuple(int(_) for _ in re.split('[-,]', line)))

    return data


def included(a, b, c, d):
    return c <= a <= d and c <= b <= d


def overlap(a, b, c, d):
    return c <= a <= d or c <= b <= d


def code1(data):
    count = 0
    for a, b, c, d in data:
        count += included(a, b, c, d) or included(c, d, a, b)
    return count


def code2(data):
    count = 0
    for a, b, c, d in data:
        count += overlap(a, b, c, d) or included(c, d, a, b)
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
