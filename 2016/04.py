"""
--- 2016 --- Day 4: Security Through Obscurity ---
"""


import re
from collections import Counter


EXAMPLES1 = (
    ('04-exemple1.txt', 123 + 987 + 404),
)

EXAMPLES2 = (
)

INPUT = '04.txt'

LOWER = 'abcdefghijklmnopqrstuvwxyz'


def read_data(filename):
    rooms = []
    with open(filename) as f:
        for line in f.readlines():
            match = re.match(r'([a-z-]+)-(\d+)\[([a-z]{5})\]', line)
            name, sectorid, check = match.group(1, 2, 3)
            rooms.append((name, sectorid, check))
    return rooms


def name_signature(name):
    counter = Counter(name.replace('-', ''))
    most_common = sorted([(1000 - count, char) for (char, count) in counter.most_common()])
    return ''.join(char for _, char in most_common)[:5]


def decrypt(name, sectorid):
    true_name = []
    for char in name:
        true_name.append(' ' if char == '-' else LOWER[(LOWER.index(char) + int(sectorid)) % 26])
    return ''.join(true_name)


def code1(rooms):
    count = 0
    for name, sectorid, check in rooms:
        signature = name_signature(name)
        if signature == check:
            count += int(sectorid)
    return count


def code2(rooms):
    assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'
    for name, sectorid, check in rooms:
        signature = name_signature(name)
        if signature == check:
            true_name = decrypt(name, sectorid)
            if 'north' in true_name:
                print(sectorid, true_name)
                return sectorid
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
