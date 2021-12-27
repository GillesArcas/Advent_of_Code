import re
import itertools


EXAMPLES1 = (
    ('19-exemple1.txt', 79),
)

EXAMPLES2 = (
    ('19-exemple1.txt', 3621),
)

INPUT = '19.txt'


def read_list(fn):
    beacons = list()
    with open(fn) as f:
        while match := re.match(r'--- scanner (\d+) ---', f.readline()):
            num = int(match.group(1))
            assert num == len(beacons), (num, len(beacons))
            beacons.append(list())
            while line := f.readline().strip():
                beacons[num].append(tuple([int(_) for _ in line.split(',')]))
    return beacons


ID = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ROTX = ((1, 0, 0), (0, 0, -1), (0, 1, 0))
ROTY = ((0, 0, -1), (0, 1, 0), (1, 0, 0))
ROTZ = ((0, 1, 0), (-1, 0, 0), (0, 0, 1))


def mulmat(mat1, mat2):
    mat = list()
    for i in range(3):
        line = list()
        for j in range(3):
            line.append(sum([mat1[i][k] * mat2[k][j] for k in range(3)]))
        mat.append(tuple(line))
    return tuple(mat)


def mulmatvec(mat, vec):
    newvec = list()
    for i in range(3):
        newvec.append(sum([mat[i][k] * vec[k] for k in range(3)]))
    return tuple(newvec)


def subvec(vec1, vec2):
    return tuple(v1 - v2 for v1, v2 in zip(vec1, vec2))


def distance(vec1, vec2):
    return abs(vec1[0] - vec2[0]) + abs(vec1[1] - vec2[1]) + abs(vec1[2] - vec2[2])


def all_transforms():
    gener = [ROTX, ROTY, ROTZ]
    trans = set(gener)
    count = 0
    while len(trans) > count:
        count = len(trans)
        trans2 = set(trans)
        for gen in gener:
            for trns in trans:
                trans2.add(mulmat(gen, trns))
        trans = trans2
    assert len(trans) == 24
    assert ID in trans
    return trans


def apply_trans(beacons, trns):
    return [mulmatvec(trns, _) for _ in beacons]


def apply_offset(beacons, offset):
    return [subvec(_, offset) for _ in beacons]


def match_beacons(beacons_ref, beacons_test):
    for bt in beacons_test:
        for br in beacons_ref:
            deltas = subvec(bt, br)
            beacons_test_shift = apply_offset(beacons_test, deltas)
            inter = set(beacons_ref).intersection(beacons_test_shift)
            if len(inter) >= 12:
                return deltas, beacons_test_shift

    return False


def search_match_beacons(index1, index2, beacons_ref, beacons1, trans):
    for trns in trans:
        beacons = apply_trans(beacons1, trns)
        if _ := match_beacons(beacons_ref, beacons):
            deltas, beacons1_shift = _
            print('match', index1, index2, deltas, trns)
            return deltas, trns, beacons1_shift
    return None


def shortest_path_to_0(index, all_matches):
    paths = set()
    paths.add((index,))
    while 1:
        newpaths = set()
        for path in paths:
            for i1, i2, _, _, _ in all_matches:
                if i2 == path[-1] and i1 not in path:
                    newpath = tuple(list(path) + [i1])
                    if i1 == 0:
                        return newpath
                    else:
                        newpaths.add(newpath)
        if newpaths == paths:
            return None
        else:
            paths = newpaths


def trans_to_scanner0(path_to_0, beacons, all_matches):
    # path_to_0: (index, ..., 0)
    for i1, i2, deltas, trns, _ in all_matches:
        if i1 == path_to_0[1] and i2 == path_to_0[0]:
            beacons = apply_trans(beacons, trns)
            beacons = apply_offset(beacons, deltas)

    if len(path_to_0) == 2:
        return beacons
    else:
        return trans_to_scanner0(path_to_0[1:], beacons, all_matches)


def code1(beacons):
    trans = all_transforms()
    all_matches = list()
    for index1, index2 in itertools.permutations(range(len(beacons)), 2):
        if _ := search_match_beacons(index1, index2, beacons[index1], beacons[index2], trans):
            deltas, trns, beacons_rotoffset = _
            all_matches.append((index1, index2, deltas, trns, beacons_rotoffset))

    all_beacons = set(beacons[0])
    for index, beacons in enumerate(beacons[1:], 1):
        path = shortest_path_to_0(index, all_matches)
        all_beacons.update(trans_to_scanner0(path, beacons, all_matches))

    return len(all_beacons)


def code2(beacons):
    trans = all_transforms()
    all_matches = list()
    for index1, index2 in itertools.permutations(range(len(beacons)), 2):
        if _ := search_match_beacons(index1, index2, beacons[index1], beacons[index2], trans):
            deltas, trns, beacons_rotoffset = _
            all_matches.append((index1, index2, deltas, trns, beacons_rotoffset))

    all_beacons = {(0, 0, 0)}
    for index, beacons in enumerate(beacons[1:], 1):
        path = shortest_path_to_0(index, all_matches)
        all_beacons.update(trans_to_scanner0(path, [(0, 0, 0)], all_matches))

    return max(distance(x, y) for x, y in itertools.combinations(all_beacons, 2))


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_list(fn)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_list(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
