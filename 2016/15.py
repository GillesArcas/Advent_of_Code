"""
--- 2016 --- Day 15: Timing is Everything ---
"""


import re


EXAMPLES1 = (
    ('15-exemple1.txt', 5),
)

EXAMPLES2 = (
)

INPUT = '15.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    disks = []
    for line in lines:
        numbers = re.findall(r'\d+', line)
        disks.append((int(numbers[1]), int(numbers[3])))
    return disks


def check_time(t, disks):
    for delay, (npos, pos_t0) in enumerate(disks, 1):
        if (pos_t0 + t + delay) % npos != 0:
            return False
    return True


def code1(disks):
    print(disks)
    for t in range(1_000_000):
        if check_time(t, disks):
            return t
    return None


def code2(disks):
    disks.append((11, 0))
    print(disks)
    for t in range(10_000_000):
        if check_time(t, disks):
            return t
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
