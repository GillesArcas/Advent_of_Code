"""
--- 2015 --- Day 16: Aunt Sue ---
"""


import re


EXAMPLES1 = (
)

EXAMPLES2 = (
)

INPUT = '16.txt'


def read_data(filename):
    aunts = {}
    with open(filename) as f:
        for line in f:
            match = re.match(r'Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)', line)
            assert match
            compounds = match.groups()[1::2]
            quantities = [int(_) for _ in match.groups()[2::2]]
            aunts[int(match.group(1))] = dict(zip(compounds, quantities))
    return aunts


KNOWN = dict(
    children= 3,
    cats= 7,
    samoyeds= 2,
    pomeranians= 3,
    akitas= 0,
    vizslas= 0,
    goldfish= 5,
    trees= 3,
    cars= 2,
    perfumes= 1
)


def code1(aunts):
    for aunt, compounds in aunts.items():
        if all(KNOWN[compound] == quantity for compound, quantity in compounds.items()):
            return aunt
    return None


def code2(aunts):
    for aunt, compounds in aunts.items():
        for compound, quantity in compounds.items():
            if compound in ('cats', 'trees'):
                if KNOWN[compound] < quantity:
                    pass
                else:
                    break
            elif compound in ('pomeranians', 'goldfish'):
                if KNOWN[compound] > quantity:
                    pass
                else:
                    break
            else:
                if KNOWN[compound] == quantity:
                    pass
                else:
                    break
        else:
            return aunt
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
