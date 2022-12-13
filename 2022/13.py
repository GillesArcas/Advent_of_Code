"""
--- 2022 --- Day 13: Distress Signal ---
"""


import re
import itertools
from functools import cmp_to_key


EXAMPLES1 = (
    ('13-exemple1.txt', 13),
)

EXAMPLES2 = (
    ('13-exemple1.txt', 140),
)

INPUT = '13.txt'


def read_data(filename):
    with open(filename) as f:
        chars = f.read()

    strpairs = re.findall(r'(\S+)\s(\S+)\s', chars)
    pairs = []
    for x, y in strpairs:
        pairs.append((eval(x), eval(y)))

    return pairs


def is_ordered(left, right):
    assert isinstance(left, list)
    assert isinstance(right, list)

    for left2, right2 in itertools.zip_longest(left, right):
        if left2 is None:
            return True
        elif right2 is None:
            return False
        elif left2 == right2:
            continue
        elif isinstance(left2, int) and isinstance(right2, int):
            return left2 < right2
        elif isinstance(left2, int):
            left2 = [left2]
            if left2 == right2:
                continue
            else:
                return is_ordered(left2, right2)
        elif isinstance(right2, int):
            right2 = [right2]
            if left2 == right2:
                continue
            else:
                return is_ordered(left2, right2)
        else:
            return is_ordered(left2, right2)
    return True


def is_ordered_cmp(left, right):
    if left == right:
        return 0
    elif is_ordered(left, right):
        return -1
    else:
        return +1


def code1(pairs):
    count = 0
    for index, (left, right) in enumerate(pairs, 1):
        if is_ordered(left, right):
            count += index
    return count


def code2(pairs):
    packets = []
    for pair in pairs:
        packets.extend(list(pair))
    packets.append([[2]])
    packets.append([[6]])
    packets = list(sorted(packets, key=cmp_to_key(is_ordered_cmp)))

    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
