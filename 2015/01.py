"""
--- 2015 --- Day 1: Not Quite Lisp ---
"""


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '01.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read()


def code1(data):
    return data.count('(') - data.count(')')


def code2(data):
    floor = 0
    for index, char in enumerate(data, 1):
        floor += 1 if char == '(' else -1
        if floor == -1:
            return index
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
