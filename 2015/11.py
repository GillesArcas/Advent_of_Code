"""
--- 2015 ---
"""


import re
from itertools import count


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '11.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def next_value(val):
    # suppose no final carry (val != 'zzzz')
    digits = list(val)
    carry = 1
    for index, digit in reversed(list(enumerate(digits))):
        if carry == 0:
            newdigit = digit
        elif digit < 'z':
            newdigit, carry = chr(ord(digit) + 1), 0
        else:
            newdigit, carry = 'a', 1
        digits[index] = newdigit
    return ''.join(digits)


def is_password(s):
    if any(_ in s for _ in 'ilo'):
        return False
    for i in range(24):
        if 'abcdefghijklmnopqrstuvwxyz'[i:i + 3] in s:
            break
    else:
        return False
    pairs = re.findall(r'(.)\1', s)
    if len(set(pairs)) < 2:
        return False
    return True


def code1(data):
    s = data
    for _ in count():
        s = next_value(s)
        if is_password(s):
            return s
    return None


def code2(data):
    s = code1(data)
    for _ in count():
        s = next_value(s)
        if is_password(s):
            return s
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
