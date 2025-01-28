"""
--- Day 22: Monkey Market ---
"""


import itertools
from collections import defaultdict


EXAMPLES1 = (
    ('22-exemple1.txt', 37327623),
)

EXAMPLES2 = (
    ('22-exemple2.txt', 23),
)

INPUT = '22.txt'


def read_data(filename):
    with open(filename) as f:
        return [int(line.strip()) for line in f.readlines()]


def next_secret(secret_number):
    secret_number = ((secret_number * 64) ^ secret_number) % 16777216
    secret_number = ((secret_number // 32) ^ secret_number) % 16777216
    secret_number = ((secret_number * 2048) ^ secret_number) % 16777216
    return secret_number


def code1(data):
    total = 0
    for x in data:
        for _ in range(2000):
            x = next_secret(x)
        total += x
    return total


def make_changes(secret):
    """
    Return dict of 4-changes and prices changes = {(-1,-1,0,2): 6, ...}
    """
    secrets = [secret]
    for _ in range(2000):
        secret = next_secret(secret)
        secrets.append(secret)

    prices = [_ % 10 for _ in secrets]
    changes = [b - a for a, b in itertools.pairwise(prices)]
    changes4 = {}
    for index, _ in enumerate(changes[:-3]):
        change = tuple(changes[index:index + 4])
        if change not in changes4:
            changes4[change] = prices[index + 4]

    return changes4


def code2(data):
    allchanges4 = defaultdict(int)
    for secret in data:
        changes4 = make_changes(secret)
        for changes, price in changes4.items():
            allchanges4[changes] += price
    return max(allchanges4.values())


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
