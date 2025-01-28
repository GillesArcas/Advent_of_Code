"""
--- Day 23: LAN Party ---

Part 2 is finding a maximal clique:
https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
https://github.com/alanmc-zz/python-bors-kerbosch/blob/master/bors-kerbosch.py
"""


import itertools
from collections import defaultdict
import re


EXAMPLES1 = (
    ('23-exemple1.txt', 7),
)

EXAMPLES2 = (
    ('23-exemple1.txt', 'co,de,ka,ta'),
)

INPUT = '23.txt'


def read_data(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    graph = defaultdict(set)
    for line in lines:
        node1 = line[:2]
        node2 = line[3:]
        graph[node1].add(node2)
        graph[node2].add(node1)
    return graph


def code1(graph):
    triangles = set()
    for node, neighbours in graph.items():
        for node1,node2 in itertools.combinations(neighbours, 2):
            if node1 in graph[node2]:
                triangle = ','.join(sorted((node, node1, node2)))
                triangles.add(triangle)

    triangles = {tri for tri in triangles if re.search(r'\bt', tri)}
    return len(triangles)


def bors_kerbosch_v1(R, P, X, G, C):

    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    for v in P.union(set([])):
        bors_kerbosch_v1(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)


def code2(graph):
    cliques = []
    bors_kerbosch_v1(set([]), set(graph.keys()), set([]), graph, cliques)
    maxclique = max(cliques, key=len)
    return ','.join(maxclique)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
