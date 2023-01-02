"""
--- 2016 --- Day 5: How About a Nice Game of Chess? ---

Keywords: md5
"""


import hashlib
import itertools


EXAMPLES1 = (
    ('05-exemple1.txt', '18f47a30'),
)

EXAMPLES2 = (
    ('05-exemple1.txt', '05ace8e3'),
)

INPUT = '05.txt'


def read_data(filename):
    with open(filename) as f:
        data = f.readlines()
    return data[0].strip()


def code1(data):
    digits = []
    s = data
    for counter in itertools.count():
        s = data + str(counter)
        h = hashlib.md5(s.encode()).hexdigest()
        if h.startswith('00000'):
            digits.append(h[5])
            print(counter, digits)
        if len(digits) == 8:
            return ''.join(digits)
    return None


def code2(data):
    digits = []
    digits2 = ['-'] * 8
    s = data
    for counter in itertools.count():
        s = data + str(counter)
        h = hashlib.md5(s.encode()).hexdigest()
        if h.startswith('00000'):
            if h[5].isdigit():
                index = int(h[5])
                if index < 8 and digits2[index] == '-':
                    digits.append(h[6])
                    digits2[index] = h[6]
                    print(counter, ''.join(digits2))
                    if len(digits) == 8:
                        return ''.join(digits2)
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


# test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
