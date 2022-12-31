"""
--- 2016 --- Day 9: Explosives in Cyberspace ---
"""


import re


EXAMPLES1 = (
    ('09-exemple1.txt', 6 + 7 + 9 + 11 + 6 + 18),
)

EXAMPLES2 = (
    ('09-exemple2.txt', 445),
)

INPUT = '09.txt'


def read_data(filename):
    with open(filename) as f:
        line = ''.join([_.strip() for _ in f.readlines()])
    return line


def code1(data):
    pointer = 0
    expended = 0
    while pointer < len(data):
        if data[pointer] != '(':
            expended += 1
            pointer += 1
        else:
            match = re.match(r'\((\d+)x(\d+)\)', data[pointer:])
            length = int(match.group(1))
            rep = int(match.group(2))
            pointer += len(match.group(0))
            expended += length * rep
            pointer += length
    return expended


def code2(data):
    pointer = 0
    expended = 0
    while pointer < len(data):
        if data[pointer] != '(':
            expended += 1
            pointer += 1
        else:
            match = re.match(r'\((\d+)x(\d+)\)', data[pointer:])
            length = int(match.group(1))
            rep = int(match.group(2))
            pointer += len(match.group(0))
            reps = data[pointer:pointer + length]
            expended += code2(reps) * rep
            pointer += length
    return expended


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
