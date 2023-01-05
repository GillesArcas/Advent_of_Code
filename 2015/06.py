"""
--- 2015 --- Day 6: Probably a Fire Hazard ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '06.txt'


def read_data(filename):
    instructions = []
    with open(filename) as f:
        for line in f.readlines():
            op = re.match('(toggle|turn off|turn on)', line).group(1)
            coords = [int(_) for _ in re.findall(r'\d+', line)]
            instructions.append([op] + coords)
    return instructions


def code1(instructions):
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for op, x1, y1, x2, y2 in instructions:
        if op == 'toggle':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = 1 - grid[y][x]
        elif op == 'turn on':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = 1
        elif op == 'turn off':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = 0
    return sum(sum(c for c in line) for line in grid)


def code2(instructions):
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for op, x1, y1, x2, y2 in instructions:
        if op == 'toggle':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = grid[y][x] + 2
        elif op == 'turn on':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = grid[y][x] + 1
        elif op == 'turn off':
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid[y][x] = max(0, grid[y][x] - 1)
    return sum(sum(c for c in line) for line in grid)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
