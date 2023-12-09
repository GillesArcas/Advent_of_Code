"""
--- Day 9: Mirage Maintenance ---
"""


EXAMPLES1 = (
    ('09-exemple1.txt', 114),
)

EXAMPLES2 = (
    ('09-exemple1.txt', 2),
)

INPUT = '09.txt'


def read_data(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append([int(_) for _ in line.split()])
    return lines


def next_difference(values):
    if all(_ == 0 for _ in values):
        return 0
    else:
        differences = [v2 - v1 for v2, v1 in zip(values[1:], values[:-1])]
        return values[-1] + next_difference(differences)


def code1(lines):
    return sum(next_difference(_) for _ in lines)


def prev_difference(values):
    if all(_ == 0 for _ in values):
        return 0
    else:
        differences = [v2 - v1 for v2, v1 in zip(values[1:], values[:-1])]
        return values[0] - prev_difference(differences)


def code2(lines):
    return sum(prev_difference(_) for _ in lines)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
