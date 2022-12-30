"""
--- 2016 --- Day 3: Squares With Three Sides ---
"""


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '03.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    return [[int(_) for _ in line.strip().split()] for line in lines]


def code1(data):
    count = 0
    for x, y, z in data:
        if x + y > z and x + z > y and y + z > x:
            count += 1
    return count


def code2(data):
    lines = [list(x) for x in zip(*data)]
    data2 = []
    for line in lines:
        for i in range(len(data) // 3):
            data2.append(line[i * 3:i * 3 + 3])
    return code1(data2)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
