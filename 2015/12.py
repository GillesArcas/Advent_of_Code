"""
--- 2015 --- Day 12: JSAbacusFramework.io ---
"""


import re
import json


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '12.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def code1(data):
    return sum(int(_) for _ in re.findall(r'-?\d+', data))


def count(x):
    if isinstance(x, str):
        return 0
    elif isinstance(x, int):
        return x
    elif isinstance(x, list):
        return sum(count(_) for _ in x)
    elif isinstance(x, dict):
        if 'red' in x.values():
            return 0
        else:
            return sum(count(_) for _ in x.values())
    else:
        assert 0, x


def code2(data):
    x = json.loads(data)
    return count(x)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
