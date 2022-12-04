"""
--- 2022 --- Day 3: Rucksack Reorganization ---
"""


EXAMPLES1 = (
    ('03-exemple1.txt', 157),
)

EXAMPLES2 = (
    ('03-exemple1.txt', 70),
)

INPUT = '03.txt'


PRIOR = '-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def read_data(filename):
    with open(filename) as f:
        data = [_.strip() for _ in f.readlines()]
    return data


def code1(data):
    count = 0
    for s in data:
        s1 = s[:len(s) // 2]
        s2 = s[len(s) // 2:]
        common = list(set(s1) & set(s2))[0]
        count += PRIOR.index(common)
    return count


def code2(data):
    count = 0
    for i in range(0, len(data), 3):
        s1, s2, s3 = data[i:i + 3]
        common = list(set(s1) & set(s2) & set(s3))[0]
        count += PRIOR.index(common)
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
