"""
--- 2016 --- Day 8: Two-Factor Authentication ---
"""


import re


EXAMPLES1 = (
    ('08-exemple1.txt', 6),
)

EXAMPLES2 = (
)

INPUT = '08.txt'


def read_data(filename):
    instructions = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            numbers = [int(_) for _ in re.findall(r'(\d+)', line)]
            for inst in ('rect', 'rotate col', 'rotate row'):
                if line.startswith(inst):
                    instructions.append((inst, *numbers))
                    continue
    return instructions


def print_grid(grid):
    for line in grid:
        print(''.join(line))
    print()


def apply(instruction, xdim, ydim, grid):
    instr, a1, a2 = instruction
    if instr == 'rect':
        for line in grid[:a2]:
            line[:a1] = '#' * a1
    elif instr == 'rotate col':
        for _ in range(a2):
            z = grid[ydim - 1][a1]
            for y in range(ydim - 1, 0, -1):
                grid[y][a1] = grid[y - 1][a1]
            grid[0][a1] = z
    elif instr == 'rotate row':
        for _ in range(a2):
            z = grid[a1][xdim - 1]
            for x in range(xdim - 1, 0, -1):
                grid[a1][x] = grid[a1][x - 1]
            grid[a1][0] = z


def code1(instructions):
    xdim, ydim = (7, 3) if len(instructions) == 4 else (50, 6)
    grid = [['.' for _ in range(xdim)] for _ in range(ydim)]
    for instruction in instructions:
        apply(instruction, xdim, ydim, grid)
        print_grid(grid)

    return sum(line.count('#') for line in grid)


def code2(_):
    pass


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
