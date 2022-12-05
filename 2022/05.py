"""
--- 2022 --- Day 5: Supply Stacks ---
"""


import re


EXAMPLES1 = (
    ('05-exemple1.txt', 'CMZ'),
)

EXAMPLES2 = (
    ('05-exemple1.txt', 'MCD'),
)

INPUT = '05.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    for index, line in enumerate(lines):
        if line.startswith(' 1 '):
            hstack = index
            match = re.search(r'(\d+)\s*$', line)
            nstack = int(match.group(1))
            break

    stacks = [[] for _ in range(nstack)]

    for line in lines[hstack - 1::-1]:
        for i in range(nstack):
            s = line[i * 4:i * 4 + 3]
            if s == '   ':
                pass
            else:
                x = s[1]
                stacks[i].append(x)

    moves = []
    for line in lines[hstack + 2:]:
        match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
        moves.append((int(match.group(1)), int(match.group(2)), int(match.group(3))))

    return stacks, moves


def code1(data):
    stacks, moves = data
    for n, ifrom, ito in moves:
        for _ in range(n):
            stacks[ito - 1].append(stacks[ifrom - 1].pop())

    return ''.join([stack[-1] for stack in stacks])


def code2(data):
    stacks, moves = data
    for n, ifrom, ito in moves:
        tmp = []
        for _ in range(n):
            tmp.append(stacks[ifrom - 1].pop())
        stacks[ito - 1].extend(reversed(tmp))

    return ''.join([stack[-1] for stack in stacks])


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
