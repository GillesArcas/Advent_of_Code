"""
--- 2016 --- Day 14: One-Time Pad ---
"""


import re
import hashlib
from functools import cache


EXAMPLES1 = (
    ('14-exemple1.txt', 22728),
)

EXAMPLES2 = (
    ('14-exemple1.txt', 22551),
)

INPUT = '14.txt'


def read_data(filename):
    with open(filename) as f:
        data = f.readlines()
    return data[0].strip()


@cache
def hashcode(salt, index, stretched=False):
    s = salt + str(index)
    h = hashlib.md5(s.encode()).hexdigest()
    if stretched:
        for _ in range(2016):
            h = hashlib.md5(h.encode()).hexdigest()
    return h


def find_key(salt, index, stretched=False):
    while True:
        h = hashcode(salt, index, stretched)
        if match := re.search(r'(\w)\1\1', h):
            target = match.group(1) * 5
            for index2 in range(index + 1, index + 1001):
                h2 = hashcode(salt, index2, stretched)
                if target in h2:
                    print(h, h2)
                    return index
        index += 1


def code1(salt):
    index = 0
    for _ in range(64):
        index = find_key(salt, index)
        print(index)
        index += 1
    return index - 1


def code2(salt):
    index = 0
    for _ in range(64):
        index = find_key(salt, index, stretched=True)
        print(index)
        index += 1
    return index - 1


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


# test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
