"""
--- 2015 ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = (2981, 3075)  # row, column


def read_data(data):
    return data


def code1(data):
    print(data)
    rowtarget, coltarget = data
    row, col = 2, 1
    code = 20151125
    while (row, col) != (rowtarget, coltarget):
        if row == 1:
            row, col = col + 1, 1
        else:
            row, col = row - 1, col + 1
        code = (code * 252533) % 33554393
    return (code * 252533) % 33554393


def code2(data):
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
