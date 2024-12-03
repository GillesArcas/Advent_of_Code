"""
--- Day 2: Red-Nosed Reports ---
"""


import itertools
from collections import Counter


EXAMPLES1 = (
    ('02-exemple1.txt', 2),
)

EXAMPLES2 = (
    ('02-exemple1.txt', 4),
)

INPUT = '02.txt'


def read_data(filename):
    reports = []
    with open(filename) as f:
        for line in f.readlines():
            reports.append([int(_) for _ in line.split()])
    return reports


def validreport1(report):
    if report == sorted(report) or report == sorted(report, reverse=True):
        for pair in itertools.pairwise(report):
            if 1 <= abs(pair[1] - pair[0]) <= 3:
                pass
            else:
                return False
    else:
        return False
    return True
    
        
def validreport2(report):
    for index, _ in enumerate(report):
        rep = report[:]
        del rep[index]
        if validreport1(rep):
            return True
    return False
    
        
def code1(reports):
    return sum(validreport1(report) for report in reports)


def code2(reports):
    return sum(validreport2(report) for report in reports)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
