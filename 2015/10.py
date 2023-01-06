"""
--- 2015 --- Day 10: Elves Look, Elves Say ---
"""


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '10.txt'


def read_data(filename):
    with open(filename) as f:
        return f.read().strip()


def next_value(val):
    val += 'xx'
    nextval = []
    index = 0
    while index < len(val) - 2:
        if val[index] == val[index + 1] == val[index + 2]:
            nextval.append('3')
            nextval.append(val[index])
            index += 3
        elif val[index] == val[index + 1]:
            nextval.append('2')
            nextval.append(val[index])
            index += 2
        else:
            nextval.append('1')
            nextval.append(val[index])
            index += 1
    return ''.join(nextval)


def code1(data):
    val = data
    for _ in range(40):
        val = next_value(val)
    return len(val)


def code2(data):
    val = data
    for _ in range(50):
        val = next_value(val)
    return len(val)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
