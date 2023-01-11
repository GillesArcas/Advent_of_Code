"""
--- 2015 --- Day 4: The Ideal Stocking Stuffer ---
"""


import hashlib
import itertools


EXAMPLES1 = (
    ('04-exemple1.txt', 609043),
)

EXAMPLES2 = (
)

INPUT = '04.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def hashcode(key, index):
    s = key + str(index)
    return hashlib.md5(s.encode()).hexdigest()


def code1(key):
    for index in itertools.count():
        if hashcode(key, index).startswith('00000'):
            return index


def code2(key):
    for index in itertools.count():
        if hashcode(key, index).startswith('000000'):
            return index


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
