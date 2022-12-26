"""
--- 2022 --- Day 25: Full of Hot Air ---
"""


import re


EXAMPLES1 = (
    ('25-exemple1.txt', '2=-1=0'),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [_.strip() for _ in f.readlines()]

    for snafu in lines:
        assert decimal_to_snafu(snafu_to_decimal(snafu)) == snafu, snafu

    return lines


def number_to_base(n, base):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.insert(0, n % base)
        n //= base
    return digits


def snafu_to_decimal(snafu):
    n = 0
    p = 1
    for index in range(len(snafu) - 1, -1, -1):
        digit = snafu[index]
        if digit == '-':
            n -= p
        elif digit == '=':
            n -= 2 * p
        else:
            n += int(digit) * p
        p *= 5
    return n


def decimal_to_snafu(n):
    digits = number_to_base(n, 5)
    for index in range(len(digits) - 1, -1, -1):
        digit = digits[index]
        if digit >= 3:
            digits[index] = '0-='[5 - digit]
            if index == 0:
                digits.insert(0, 1)
            else:
                digits[index - 1] += 1
    return ''.join([str(_) for _ in digits])


def code1(lines):
    total = 0
    for snafu in lines:
        total += snafu_to_decimal(snafu)
    return decimal_to_snafu(total)


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
