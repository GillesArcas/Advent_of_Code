"""
--- 2015 --- Day 20: Infinite Elves and Infinite Houses ---
"""


from itertools import count
from collections import defaultdict


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = 34000000


def read_data(data):
    return data


def sum_of_divisors(n):
    sd = 1
    i = 2
    while i * i <= n:
        if n % i == 0:
            d2 = n // i
            if d2 == i:
                sd += i
            else:
                sd += i + d2
        i += 1
    return sd


def code1(data):
    for n in count(2):
        if n % 100000 == 0:
            print(n)
        s = (sum_of_divisors(n) + n) * 10
        if s >= data:
            return n
    return None


def code2(data):
    presents = defaultdict(int)
    elfmax = 1_000_000_000
    elf = 1
    while elf < elfmax:
        for numhouse in range(1, 51):
            index = elf * numhouse
            presents[index] += 11 * elf
            if presents[index] >= data and index < elfmax:
                elfmax = index
                print(elfmax)
        elf += 1

    return elfmax


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
