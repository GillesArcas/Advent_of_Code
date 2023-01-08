"""
--- 2015 --- Day 19: Medicine for Rudolph ---
"""


import re


EXAMPLES1 = (
    ('19-exemple1.txt', 4),
)

EXAMPLES2 = (
)

INPUT = '19.txt'


def read_data(filename):
    with open(filename) as f:
        lines = f.readlines()
    rules = [line.strip().split(' => ') for line in lines[:-2]]
    molecule = lines[-1].strip()
    return rules, molecule


def code1(data):
    rules, molecule = data
    molecules = set()

    for lhs, rhs in rules:
        for match in re.finditer(lhs, molecule):
            newmol = molecule[:match.start()] + rhs + molecule[match.end():]
            molecules.add(newmol)

    return len(molecules)


def check(rules, molecule):
    stack = []
    stack.append((molecule, 0))
    dejavu = set()
    while stack:
        mol, nsteps = stack.pop(0)
        if mol == '' or mol == 'e':
            return mol, nsteps
        for lhs, rhs in rules:
            for match in re.finditer(rhs, mol):
                newmol = mol[:match.start()] + lhs + mol[match.end():]
                if newmol in dejavu:
                    continue
                dejavu.add(newmol)
                stack.append((newmol, nsteps + 1))

    return mol, nsteps

def check_fragments(rules, molecule):
    count = 0
    redmol = ''
    for submol in molecule.split('Ar'):
        mol, nsteps = check(rules, submol + 'Ar')
        redmol += mol
        count += nsteps
        print(mol)
    return redmol, count


def code2(data):
    rules, molecule = data
    rules = sorted(rules, reverse=True, key= lambda x: len(x[1]))

    redmol1, count1 = check_fragments(rules, molecule)
    print(redmol1)
    redmol2, count2 = check_fragments(rules, redmol1)
    print(redmol2)
    _, nsteps = check(rules, redmol2)
    return count1 + count2 + nsteps


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
