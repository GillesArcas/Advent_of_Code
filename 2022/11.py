"""
--- 2022 --- Day 11: Monkey in the Middle ---
"""


import re
import math


EXAMPLES1 = (
    ('11-exemple1.txt', 10605),
)

EXAMPLES2 = (
    ('11-exemple1.txt', 2713310158),
)

INPUT = '11.txt'


PATTERN = r"""Monkey (\d+):
  Starting items: ([0-9, ]+)
  Operation: new = old ([+*]) (\d+|old)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)
"""


def read_data(filename):
    with open(filename) as f:
        notes = re.findall(PATTERN, f.read())

    data = []
    for _, stress_list, op, operand, *numbers in notes:
        x = [int(_) for _ in stress_list.split(', ')]
        y = 'old' if operand == 'old' else int(operand)
        z = [int(_) for _ in numbers]
        data.append((x, op, y, *z))

    return data


def run_monkey(monkey, mdata, data, inspected, part, modulo):
    lstress, op, operand, divisor, monkey_t, monkey_f = mdata
    for stress in lstress:
        if operand == 'old':
            x = stress
        else:
            x = operand
        if op == '+':
            new = stress + x
        else:
            new = stress * x

        if part == 1:
            new //= 3
        else:
            new %= modulo

        if new % divisor == 0:
            data[monkey_t][0].append(new)
        else:
            data[monkey_f][0].append(new)

    inspected[monkey] += len(lstress)
    lstress.clear()


def run_round(data, inspected, part):
    modulo = math.prod((_[3] for _ in data))
    for monkey, mdata in enumerate(data):
        run_monkey(monkey, mdata, data, inspected, part, modulo)


def code1(data):
    inspected = [0] * len(data)
    for _ in range(20):
        run_round(data, inspected, part=1)
    inspected = sorted(inspected, reverse=True)
    return inspected[0] * inspected[1]


def code2(data):
    inspected = [0] * len(data)
    for _ in range(1, 10001):
        run_round(data, inspected, part=2)
        if _ % 1000 == 0:
            print(_, inspected)
    inspected = sorted(inspected, reverse=True)
    return inspected[0] * inspected[1]


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
