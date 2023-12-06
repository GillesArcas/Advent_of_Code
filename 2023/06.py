"""
--- Day 6: Wait For It ---
"""


import re


EXAMPLES1 = (
    ('06-exemple1.txt', 288),
)

EXAMPLES2 = (
    ('06-exemple1.txt', 71503),
)

INPUT = '06.txt'


def read_data(filename):
    with open(filename) as f:
        times = [int(_) for _ in re.findall(r'\d+', f.readline())]
        distances = [int(_) for _ in re.findall(r'\d+', f.readline())]
    return times, distances


def code1(data):
    times, distances = data
    winprod = 1
    for time, distance in zip(times, distances):
        wins = sum(t * (time - t) > distance for t in range(1, time))
        winprod *= wins
    return winprod


def code2(data):
    return code1([[int(''.join(map(str, _)))] for _ in data])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
