"""
--- Day 11: Plutonian Pebbles ---
"""


import functools


EXAMPLES1 = (
    ('11-exemple1.txt', 55312),
)

EXAMPLES2 = (
)

INPUT = '11.txt'


def read_data(filename):
    with open(filename) as f:
        return [int(_) for _ in f.readline().strip().split()]


def calc(data, nblinks):
    for blink in range(1, nblinks + 1):
        newdata = []
        for x in data:
            if x == 0:
                newdata.append(1)
            else:
                sx = str(x)
                if len(sx) % 2 == 0:
                    newdata.append(int(sx[:len(sx) // 2]))
                    newdata.append(int(sx[len(sx) // 2:]))
                else:
                    newdata.append(2024 * x)
        data = newdata
    return len(data)


def code1(data):
    return calc(data, 25)


@functools.cache
def calcval(x, nblinks, target):
    if nblinks == target:
        return 1
    else:
        if x == 0:
            return calcval(1, nblinks + 1, target)
        else:
            sx = str(x)
            if len(sx) % 2 == 0:
                return calcval(int(sx[:len(sx) // 2]), nblinks + 1, target) +\
                       calcval(int(sx[len(sx) // 2:]), nblinks + 1, target)
            else:
                return calcval(2024 * x, nblinks + 1, target)


def code2(data):
    return sum(calcval(_, 0, 75) for _ in data)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
