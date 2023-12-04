"""
--- Day 4: Scratchcards ---
"""


import re


EXAMPLES1 = (
    ('04-exemple1.txt', 13),
)

EXAMPLES2 = (
    ('04-exemple1.txt', 30),
)

INPUT = '04.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()

    data = []
    for line in (_.strip() for _ in lines):
        print(line)
        match = re.match(r'Card +(\d+): ([^|]+)\|([^|]+)', line)
        cardnum = match.group(1)
        list1 = [int(_) for _ in match.group(2).split()]
        list2 = [int(_) for _ in match.group(3).split()]
        data.append((cardnum, list1, list2))
    return data


def code1(data):
    score = 0
    for cardnum, list1, list2 in data:
        inter = set(list1).intersection(set(list2))
        if len(inter) > 0:
            score += pow(2, len(inter) - 1)
    return score


def code2(data):
    numcards = [1] * len(data)
    for index, (cardnum, list1, list2) in enumerate(data):
        inter = set(list1).intersection(set(list2))
        if len(inter) > 0:
            for k in range(1, len(inter) + 1):
                if index + k < len(data):
                    numcards[index + k] += numcards[index]
    return sum(numcards)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
