"""
--- 2016 --- Day 7: Internet Protocol Version 7 ---
"""


import re


EXAMPLES1 = (
    ('07-exemple1.txt', 2),
)

EXAMPLES2 = (
    ('07-exemple2.txt', 3),
)

INPUT = '07.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def code1(lines):
    count = 0
    for line in lines:
        inside = ''.join(re.findall(r'\[[a-z]+?\]', line))
        match = re.search(r'([a-z])([a-z])\2\1', inside)
        if match and match.group(1) != match.group(2):
            continue

        outside = re.sub(r'\[[a-z]+?\]', ' ', line)
        match = re.search(r'([a-z])([a-z])\2\1', outside)
        if match and match.group(1) != match.group(2):
            count += 1
    return count


def code2(lines):
    count = 0
    for line in lines:
        inside = ''.join(re.findall(r'\[[a-z]+?\]', line))
        outside = re.sub(r'\[[a-z]+?\]', ' ', line)

        abalist = re.findall(r'(?=([a-z])([a-z])(\1))', outside)
        abalist = [x for x in abalist if x[0] != x[1]]

        for a, b, _ in abalist:
            if b + a + b in inside:
                count += 1
                break
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
