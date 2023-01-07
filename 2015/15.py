
"""
--- 2015 --- Day 15: Science for Hungry People ---
"""


import re


EXAMPLES1 = (
    ('15-exemple1.txt', 62842880),
)

EXAMPLES2 = (
    ('15-exemple1.txt', 57600000),
)

INPUT = '15.txt'


def read_data(filename):
    ingredients = {}
    with open(filename) as f:
        for line in f:
            name = line.split(':', 1)[0]
            ingredients[name] = [int(_) for _ in re.findall(r'-?\d+', line)]
    return ingredients


def partitions(n, p):
    if p == 2:
        for a in range(n + 1):
            yield a, n - a
    elif p == 4:
        for a in range(n + 1):
            for b in range(n - a + 1):
                for c in range(n - (a + b) + 1):
                    yield a, b, c, n - (a + b + c)
    else:
        assert 0


def code1(ingredients):
    maxi = 0
    for partition in partitions(100, len(ingredients)):
        score = 1
        for ingredient in range(4):
            s = sum(k * ingredients[name][ingredient] for (name, k) in zip(ingredients, partition))
            score *= max(0, s)
        if score > maxi:
            maxi = score
    return maxi


def code2(ingredients):
    maxi = 0
    for partition in partitions(100, len(ingredients)):
        score = 1
        for ingredient in range(4):
            s = sum(k * ingredients[name][ingredient] for (name, k) in zip(ingredients, partition))
            score *= max(0, s)
        calories = sum(k * ingredients[name][4] for (name, k) in zip(ingredients, partition))
        if calories == 500 and score > maxi:
            maxi = score
    return maxi


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
