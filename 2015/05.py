"""
--- 2015 --- Day 5: Doesn't He Have Intern-Elves For This? ---
"""


import re


EXAMPLES1 = (
    # ('05-exemple1.txt', None),
)

EXAMPLES2 = (
)

INPUT = '05.txt'


def read_data(filename):
    with open(filename) as f:
        return [_.strip() for _ in f.readlines()]


def isnice1(string):
    if len(re.findall('[aeiou]', string)) < 3:
        return False
    if not re.search(r'(.)\1', string):
        return False
    if any(_ in string for _ in ('ab', 'cd', 'pq', 'xy')):
        return False
    return True


def isnice2(string):
    if not re.search(r'(..).*\1', string):
        return False
    if not re.search(r'(.).\1', string):
        return False
    return True



def code1(strings):
    return sum(isnice1(_) for _ in strings)


def code2(strings):
    return sum(isnice2(_) for _ in strings)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
