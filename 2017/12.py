import re


EXAMPLES1 = (
    ('12-exemple1.txt', 6),
)

EXAMPLES2 = (
    ('12-exemple1.txt', 2),
)

INPUT = '12.txt'


def read_data(fn):
    nodes = dict()
    with open(fn) as f:
        for line in f:
            match = re.match(r'(\d+) <-> (.*)', line)
            nodes[int(match.group(1))] = [int(_) for _ in match.group(2).split(', ')]
    return nodes


def group(nodes, node):
    composantes = set()
    nextnodes = list()
    nextnodes.append(node)
    while nextnodes:
        node = nextnodes.pop()
        if node not in composantes:
            composantes.add(node)
            nextnodes.extend(nodes[node])
    return composantes


def code1(data):
    nodes = data
    return len(group(nodes, 0))


def code2(data):
    nodes = data
    listnodes = list(nodes)
    nb_group = 0
    while listnodes:
        nb_group += 1
        node = listnodes.pop(0)
        compo = group(nodes, node)
        listnodes = [node for node in listnodes if node not in compo]
    return nb_group


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
