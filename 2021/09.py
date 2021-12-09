
EXAMPLES1 = (
    ('09-exemple1.txt', 15),
)

EXAMPLES2 = (
    ('09-exemple1.txt', 1134),
)

INPUT =  '09.txt'


def read_data(fn):
    data = list()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            data.append(line)
    return data


def neighbours(data, i, j):
    neigh = ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
    return [x for x in neigh if 0 <= x[0] < len(data) and 0 <= x[1] < len(data[0])]


def low_points(data):
    points = list()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if all(data[i2][j2] > c for i2, j2 in neighbours(data, i, j)):
                points.append((i, j))
    return points


def code1(data):
    score = 0
    for i, j in low_points(data):
        score += int(data[i][j]) + 1
    return score


def make_bassin(data, bassin, i, j):
    for i2, j2 in neighbours(data, i, j):
        if (i2, j2) in bassin or data[i2][j2] == '9':
            pass
        else:
            bassin.add((i2, j2))
            bassin = make_bassin(data, bassin, i2, j2)
    return bassin


def code2(data):
    size_bassins = list()
    for i, j in low_points(data):
        bassin = set()
        bassin.add((i, j))
        bassin = make_bassin(data, bassin, i, j)
        size_bassins.append(len(bassin))

    x, y, z = sorted(size_bassins, reverse=True)[:3]
    return x * y * z


def test(n, code, examples, myinput):
    for fn, result in examples:
        data = read_data(fn)
        assert result is None or code(data) == result, (data, result, code(data))

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
