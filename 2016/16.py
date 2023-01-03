"""
--- 2016 --- Day 16: Dragon Checksum ---
"""


EXAMPLES1 = (
    ('16-exemple1.txt', '01100'),
)

EXAMPLES2 = (
)

INPUT = '16.txt'


def read_data(filename):
    with open(filename) as f:
        binstr, size = f.read().split()
    return binstr, int(size)


def dragon_step(binstr):
    a = binstr
    b = ''.join(['0' if c == '1' else '1' for c in reversed(a)])
    return a + '0' + b


def dragon_cover(binstr, size):
    while len(binstr) < size:
        binstr = dragon_step(binstr)
    return binstr[:size]


def checksum(string):
    x = [('0', '1')[c1 == c2] for c1, c2 in zip(string[::2], string[1::2])]
    if len(x) % 2 == 0:
        return checksum(x)
    else:
        return ''.join(x)


def code1(data):
    binstr, size = data
    string = dragon_cover(binstr, size)
    check = checksum(string)
    return check


def code2(data):
    binstr, size = data
    size = 35651584
    return code1((binstr, size))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
