"""
--- 2015 --- Day 8: Matchsticks ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '08.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def code1(strings):
    count = 0
    for string in strings:
        s = string[1:-1]
        s = s.replace(r'\\', '\\')
        s = s.replace(r'\"', '"')
        s = re.sub(r'\\x[0-9a-f][0-9a-f]', '@', s)
        # print('%-40s %s' % (string, s))
        count += len(string) - len(s)
    return count


def code2(strings):
    count = 0
    for string in strings:
        ls = []
        for c in string:
            if c == '"':
                ls.extend(['\\', '"'])
            elif c == '\\':
                ls.extend(['\\', '\\'])
            else:
                ls.append(c)
        s = ''.join(['"'] + ls + ['"'])
        # print('%-40s %s' % (string, s))
        count += len(s) - len(string)
    return count


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
