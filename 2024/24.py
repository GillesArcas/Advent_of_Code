"""
--- Day 24: Crossed Wires ---
"""


import re
import random


EXAMPLES1 = (
    ('24-exemple1.txt', 4),
    ('24-exemple2.txt', 2024),
)

EXAMPLES2 = (
)

INPUT = '24.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.read()
    inputs = {}
    for var, val in re.findall(r'(\w+): (\d)', lines):
        inputs[var] = int(val)
    rules = {}
    for op1, op, op2, r in re.findall(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)', lines):
        rules[r] = (op, op1, op2)
    outputs = []
    outputs = sorted([r for r in rules if r[0] == 'z'], reverse=True)
    return inputs, rules, outputs


def getvalue(x, inputs, rules):
    if x in inputs:
        return inputs[x]
    else:
        op, op1, op2 = rules[x]
        val1 = getvalue(op1, inputs, rules)
        val2 = getvalue(op2, inputs, rules)
        if op == 'AND':
            return val1 & val2
        elif op == 'OR':
            return val1 | val2
        elif op == 'XOR':
            return val1 ^ val2
        else:
            assert 0


def code1(data):
    inputs, rules, outputs = data
    result = [getvalue(x, inputs, rules) for x in outputs]
    return int(''.join([str(_) for _ in result]), base=2)


ADDER = {
    'r1': ('XOR', 'x', 'y'),
    'c1': ('AND', 'x', 'y'),
    'r':  ('XOR', 'carry', 'r1'),
    'c2': ('AND', 'carry', 'r1'),
    'c':  ('OR', 'c1', 'c2'),
}


def encode_to_graphviz(rules, filename):
    with open(filename, 'wt') as f:
        print('digraph G {', file=f)
        for index, (r, (op, op1, op2)) in enumerate(rules.items()):
            print(f'{op1} -> {op}{index};', file=f)
            print(f'{op2} -> {op}{index};', file=f)
            print(f'{op}{index} -> {r};', file=f)
        print('}', file=f)


def find_rule(input1, input2, logic, rules):
    for r, (op, op1, op2) in rules.items():
        if op == logic and {op1, op2} == {input1, input2}:
            return r
    else:
        return None


def find_adder(input1, input2, carry, rules):
    if (r1 := find_rule(input1, input2, 'XOR', rules)) is None:
        return None
    if (c1 := find_rule(input1, input2, 'AND', rules)) is None:
        return None
    if (r := find_rule(r1, carry, 'XOR', rules)) is None:
        return None
    if (c2 := find_rule(r1, carry, 'AND', rules)) is None:
        return None
    if (c := find_rule(c1, c2, 'OR', rules)) is None:
        return None
    return r, c


def code2(data):
    inputs, rules, outputs = data

    # FIX
    # Found visually, one by one. If the structure of a full adder is not detected,
    # the error message gives the inputs. The graph is analized with graphviz.
    fix = (('z10', 'vcf'), ('z17', 'fhg'), ('dvb', 'fsq'), ('tnc', 'z39'))
    for a, b in fix:
        rules[a], rules[b] = rules[b], rules[a]

    # encode_to_graphviz(ADDER, 'adder.dot')
    # encode_to_graphviz(rules, 'graph.dot')

    carry = 'kvj'
    for rang in range(1, 45):
        x = 'x%02d' % rang
        y = 'y%02d' % rang
        if (adder := find_adder(x, y, carry, rules)) is None:
            print('Adder', x, y, carry, 'not found')
            exit()
        r, carry = adder

    # fixed, check
    for _ in range(1000):
        x = random.choices((0, 1), k=45)                # high to low bits
        y = random.choices((0, 1), k=45)
        xn = int(''.join([str(_) for _ in x]), base=2)
        yn = int(''.join([str(_) for _ in y]), base=2)
        r = xn + yn                                     # expected result

        for rang, bit in zip(range(45), reversed(x)):   # feed first input number
            inputs['x%02d' % rang] = bit
        for rang, bit in zip(range(45), reversed(y)):   # feed second input number
            inputs['y%02d' % rang] = bit

        z = [getvalue('z%02d' % rang, inputs, rules) for rang in range(46)]
        z = int(''.join([str(_) for _ in reversed(z)]), base=2)

        assert r == z, (_, r, z)

    return ','.join(sorted(sum(fix, ())))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
