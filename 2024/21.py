"""
--- Day 21: Keypad Conundrum ---
"""


import itertools
import functools
from collections import defaultdict
from frozendict import frozendict

from icecream import ic

EXAMPLES1 = (
    ('21-exemple1.txt', 126384),
)

EXAMPLES2 = (
)

INPUT = '21.txt'


def read_data(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


NUMPOS = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
                 '0': (3, 1), 'A': (3, 2),
}

DIRPOS = {
                 '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}


IDELTA = {'<': 0, '>': 0, '^': -1, 'v': 1}
JDELTA = {'<': -1, '>': 1, '^': 0, 'v': 0}


def key_to_key_moves(keypos):
    """
    keypos: positions of keys, NUMPOS or DIRPOS
    moves[key1, key2] = moves (<>^v) from key1 to key2
    """
    moves = defaultdict(list)
    for key1 in keypos:
        for key2 in keypos:
            i1, j1 = keypos[key1]
            i2, j2 = keypos[key2]
            ver = 'v' * (i2 - i1) if i2 > i1 else '^' * (i1 - i2)
            hor = '>' * (j2 - j1) if j2 > j1 else '<' * (j1 - j2)
            if checkmoves(key1, hor + ver, keypos):
                moves[key1, key2].append(hor + ver)
            if hor and ver and checkmoves(key1, ver + hor, keypos):
                moves[key1, key2].append(ver + hor)
            moves[key1, key2] = tuple(moves[key1, key2])

    return frozendict(moves)


def checkmoves(key, moves, keypos):
    """
    Detect key sequences passing through gap.
    """
    pos = keypos[key]
    for move in moves:
        if pos not in keypos.values():
            return False
        else:
            pos = nextpos(pos, move)
    return True


def nextpos(pos, move):
    return pos[0] + IDELTA[move], pos[1] + JDELTA[move]


def shortest(liste):
    minlen = min(len(_) for _ in liste)
    return {_ for _ in liste if len(_) == minlen}


def moves_for_pad(seq, moves):
    seq = 'A' + seq
    listkeys = set()
    stack = []
    stack.append(('', 0))
    while stack:
        keys, index = stack.pop()
        a = seq[index]
        b = seq[index + 1]
        for keys2 in moves[a, b]:
            if index == len(seq) - 2:
                listkeys.add(keys + keys2 + 'A')
            else:
                stack.append((keys + keys2 + 'A', index + 1))

    return shortest(listkeys)


@functools.cache
def moves_for_pad_rec(seq, index, moves):
    if index == len(seq) - 1:
        return {''}
    else:
        a = seq[index]
        b = seq[index + 1]
        sol = set()
        for keys in moves[a, b]:
            sol2 = {keys + 'A' + _ for _ in moves_for_pad_rec(seq, index + 1, moves)}
            sol = sol.union(sol2)
        return sol


def moves_for_pad(seq, moves):
    return moves_for_pad_rec('A' + seq, 0, moves)


def getkeys(code, numdir, movesnum, movesdir):
    """
    Iteration on moves_for_pad
    """
    listkeys = moves_for_pad(code, movesnum)
    minlen = float('inf')
    for _ in range(numdir):
        listkeys2 = set()
        for seq in listkeys:
            listkeys2.update(moves_for_pad(seq, movesdir))
        listkeys = shortest(listkeys2)
    return listkeys


@functools.cache
def lenmoves(seq, moves, target_level, current_level=0):
    if current_level == target_level:
        return len(seq)
    else:
        length = 0
        for a, b in itertools.pairwise('A' + seq):
            length2 = float('inf')
            for keys in moves[a, b]:
                length2 = min(length2, lenmoves(keys + 'A', moves, target_level, current_level + 1))
            length += length2
        return length


def getlens(code, numdir, movesnum, movesdir):
    listkeys = moves_for_pad(code, movesnum)
    minlen = float('inf')
    for seq in listkeys:
        minlen = min(minlen, lenmoves(seq, movesdir, numdir, 0))
    return minlen


def code1(data):
    movesnum = key_to_key_moves(NUMPOS)
    movesdir = key_to_key_moves(DIRPOS)
    numdir = 2
    comp = 0
    for codein in data:
        keys = getkeys(codein, numdir, movesnum, movesdir)
        comp += len(list(keys)[0]) * int(codein[:-1])
    return comp


def code2(data):
    movesnum = key_to_key_moves(NUMPOS)
    movesdir = key_to_key_moves(DIRPOS)
    numdir = 25
    comp = 0
    for codein in data:
        length = getlens(codein, numdir, movesnum, movesdir)
        print(codein, length)
        comp += length * int(codein[:-1])
    return comp


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
