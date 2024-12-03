"""
--- Day 1: Historian Hysteria ---
"""


from collections import Counter

EXAMPLES1 = (
    ('01-exemple1.txt', 11),
)

EXAMPLES2 = (
    ('01-exemple1.txt', 31),
)

INPUT = '01.txt'


def read_data(filename):
    l1, l2 = [], []
    with open(filename) as f:
        for line in f.readlines():
            n1, n2 = [int(_) for _ in line.split()]
            l1.append(n1)
            l2.append(n2)
    return l1, l2


def code1(lists):
    l1, l2 = lists
    return sum(abs(n1 - n2) for n1, n2 in zip(sorted(l1), sorted(l2)))


def code2(lists):
    l1, l2 = lists
    count = Counter(l2)
    return sum(n * count[n] for n in l1 if n in l2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
