"""
--- Day 1: Trebuchet?! ---
"""


import re


EXAMPLES1 = (
    ('01-exemple1.txt', 142),
)

EXAMPLES2 = (
    ('01-exemple2.txt', 281),
)

INPUT = '01.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


def code1(lines):
    return sum([int(ints[0] + ints[-1]) for ints in [re.findall('\d', line) for line in lines]])


def findfirst(line):
    digits = 'one|two|three|four|five|six|seven|eight|nine'
    match = re.search(r'\d' + '|' + digits, line)
    if not match:
        print(line)
    if match.group(0).isdigit():
        return int(match.group(0))
    else:
        return digits.split('|').index(match.group(0)) + 1


def findlast(line):
    digits = 'one|two|three|four|five|six|seven|eight|nine'
    match = re.search(r'\d' + '|' + digits[::-1], line[::-1])
    if match.group(0).isdigit():
        return int(match.group(0))
    else:
        return digits.split('|').index(match.group(0)[::-1]) + 1


def code2(lines):
    return sum(10 * findfirst(line) + findlast(line) for line in lines)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
