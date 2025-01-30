"""
--- Day 25: Code Chronicle ---
"""


import re
import itertools


EXAMPLES1 = (
    # ('25-exemple1.txt', 3),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.read()

    locks = re.findall(r'#####\n(?:[.#]{5}\n){5}[.]{5}\n', lines)
    locksn = []
    for lock in locks:
        locksn.append([col.count('#') - 1 for col in zip(*[list(line) for line in lock.splitlines()])])

    keys = re.findall(r'[.]{5}\n(?:[.#]{5}\n){5}#####\n', lines)
    keysn = []
    for key in keys:
        keysn.append([col.count('#') - 1 for col in zip(*[list(line) for line in key.splitlines()])])

    return locksn, keysn


def code1(data):
    locks, keys = data
    count = 0
    for lock, key in itertools.product(locks, keys):
        if all(x + y <= 5 for x, y in zip(lock, key)):
            count += 1
    return count


def code2(data):
    return 0


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
