"""
--- 2016 --- Day 1: No Time for a Taxicab ---
"""


import re


EXAMPLES1 = (
    ('01-exemple1.txt', 12),
)

EXAMPLES2 = (
    ('01-exemple2.txt', 4),
)

INPUT = '01.txt'


def read_data(filename):
    with open(filename) as f:
        line = f.read()
    data = [(x[0], int(x[1:])) for x in re.findall(r'([LR]\d+)', line)]
    return data


NEWDIR = {'N': {'L': 'W', 'R': 'E'}, 'E': {'L': 'N', 'R': 'S'},
          'S': {'L': 'E', 'R': 'W'}, 'W': {'L': 'S', 'R': 'N'}}


def code1(data):
    x, y, direction = 0, 0, 'N'
    for turn, steps in data:
        direction = NEWDIR[direction][turn]
        if direction == 'N':
            y -= steps
        elif direction == 'S':
            y += steps
        elif direction == 'W':
            x -= steps
        elif direction == 'E':
            x += steps
    return abs(x) + abs(y)


def code2(data):
    x, y, direction = 0, 0, 'N'
    locations = {(x, y)}
    for turn, steps in data:
        direction = NEWDIR[direction][turn]
        if direction == 'N':
            for _ in range(steps):
                y -= 1
                if (x, y) in locations:
                    return abs(x) + abs(y)
                else:
                    locations.add((x, y))
        elif direction == 'S':
            for _ in range(steps):
                y += 1
                if (x, y) in locations:
                    return abs(x) + abs(y)
                else:
                    locations.add((x, y))
        elif direction == 'W':
            for _ in range(steps):
                x -= 1
                if (x, y) in locations:
                    return abs(x) + abs(y)
                else:
                    locations.add((x, y))
        elif direction == 'E':
            for _ in range(steps):
                x += 1
                if (x, y) in locations:
                    return abs(x) + abs(y)
                else:
                    locations.add((x, y))
    return 0


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
