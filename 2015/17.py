"""
--- 2015 --- Day 17: No Such Thing as Too Much ---
"""


from itertools import combinations


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '17.txt'


def read_data(filename):
    with open(filename) as f:
        return [int(_) for _ in f.readlines()]


def fill(size, containers):
    count = 0
    for number in range(1, len(containers) + 1):
        found_lower = False
        for sol in combinations(range(len(containers)), number):
            sizesol = sum(containers[_] for _ in sol)
            if sizesol == size:
                count += 1
            if sizesol <= size:
                found_lower = True
        if found_lower is False:
            break
    return count


def fill_min(size, containers):
    count = 0
    for number in range(1, len(containers) + 1):
        print(number)
        for sol in combinations(range(len(containers)), number):
            sizesol = sum(containers[_] for _ in sol)
            if sizesol == size:
                count += 1
        if count:
            break
    return count


def code1(containers):
    return fill(150, containers)


def code2(containers):
    return fill_min(150, containers)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
