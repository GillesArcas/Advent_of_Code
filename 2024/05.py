"""
--- Day 5: Print Queue ---
"""


EXAMPLES1 = (
    ('05-exemple1.txt', 143),
)

EXAMPLES2 = (
    ('05-exemple1.txt', 123),
)

INPUT = '05.txt'


def read_data(filename):
    order = []
    updates = []
    with open(filename) as f:
        for line in f:
            if '|' in line:
                order.append([int(_) for _ in line.strip().split('|')])
            if ',' in line:
                updates.append([int(_) for _ in line.strip().split(',')])
    return order, updates


def isvalid(update, order):
    for n1, n2 in order:
        if n1 in update and n2 in update:
            if not update.index(n1) < update.index(n2):
                return False
    return True


def code1(data):
    order, updates = data
    result = 0
    for update in updates:
        if isvalid(update, order):
            result += update[len(update) // 2]
    return result


def code2(data):
    order, updates = data
    result = 0
    for update in updates:
        if isvalid(update, order):
            continue
        updict = {}
        for index, n in enumerate(update):
            updict[n] = set(update[index + 1:])
        for n1, n2 in order:
            if n2 in updict and n1 in updict[n2]:
                updict[n2].remove(n1)
                updict[n1].add(n2)
        new = [0] * len(update)
        for n, succ in updict.items():
            new[len(succ)] = n
        new = list(reversed(new))
        result += new[len(update) // 2]

    return result


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
