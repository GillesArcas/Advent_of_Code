import re


EXAMPLES1 = (
    ('target area: x=20..30, y=-10..-5', 45),
)

EXAMPLES2 = (
    ('target area: x=20..30, y=-10..-5', 112),
)

INPUT =  'target area: x=124..174, y=-123..-86'


def read_data(s):
    match = re.match(r'target area: x=(\d+)\.\.(\d+), y=(-\d+)\.\.(-\d+)', s)
    return [int(_) for _ in match.group(1, 2, 3, 4)]


def maxlaunch(dx0, dy0, x1, x2, y1, y2):
    x = y = 0
    maxy = 0
    dx, dy = dx0, dy0
    while 1:
        x += dx
        y += dy
        dx = max(0, dx - 1)
        dy -= 1
        if y > maxy:
            maxy = y
        if x > x2 or y < y1:
            return -float('inf')
        if x1 <= x <= x2 and y1 <= y <= y2:
            return maxy


def code1(data):
    x1, x2, y1, y2 = data
    maxy = 0
    for dx in range(1, x2 + 1):
        for dy in range(1, 1000):
            maxy = max(maxy, maxlaunch(dx, dy, x1, x2, y1, y2))
    return maxy


def code2(data):
    x1, x2, y1, y2 = data
    count = 0
    for dx in range(1, x2 + 1):
        for dy in range(-1000, 1000):
            if maxlaunch(dx, dy, x1, x2, y1, y2) > -float('inf'):
                count += 1
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
