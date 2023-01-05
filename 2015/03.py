"""
--- 2015 --- Day 3: Perfectly Spherical Houses in a Vacuum ---
"""


EXAMPLES1 = (
    ('03-exemple1.txt', 4),
)

EXAMPLES2 = (
    ('03-exemple1.txt', 3),
)

INPUT = '03.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def next_pos(x, y, c):
    if c == '^':
        y -= 1
    elif c == 'v':
        y += 1
    elif c == '<':
        x -= 1
    elif c == '>':
        x += 1
    return x, y


def code1(data):
    count = 0
    visited = set()
    x, y = 0, 0
    count += 1
    visited.add((x, y))
    for c in data:
        x, y = next_pos(x, y, c)
        if (x, y) not in visited:
            count += 1
            visited.add((x, y))
    return count


def code2(data):
    count = 0
    visited = set()
    x1, y1 = 0, 0
    count += 1
    visited.add((x1, y1))
    x2, y2 = 0, 0
    for c1, c2 in zip(data[::2], data[1::2]):
        x1, y1 = next_pos(x1, y1, c1)
        if (x1, y1) not in visited:
            count += 1
            visited.add((x1, y1))
        x2, y2 = next_pos(x2, y2, c2)
        if (x2, y2) not in visited:
            count += 1
            visited.add((x2, y2))
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
