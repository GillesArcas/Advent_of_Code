
EXAMPLES1 = (
    ('24-exemple1.txt', 31),
)

EXAMPLES2 = (
    ('24-exemple1.txt', 19),
)

INPUT = '24.txt'


def read_data(data):
    adjacency = dict()
    with open(data) as f:
        for line in f:
            x, y = [int(_) for _ in line.strip().split('/')]
            if x not in adjacency:
                adjacency[x] = dict()
            adjacency[x][y] = x + y
            if y not in adjacency:
                adjacency[y] = dict()
            adjacency[y][x] = x + y
    return adjacency


def max_bridge1(start, adjacency):
    maxi = 0
    for nextn in adjacency[start]:
        weight = adjacency[start][nextn]
        if weight == 0:
            continue
        adjacency[start][nextn] = 0
        adjacency[nextn][start] = 0
        strength = weight + max_bridge1(nextn, adjacency)
        if strength > maxi:
            maxi = strength
        adjacency[start][nextn] = weight
        adjacency[nextn][start] = weight
    return maxi


def max_bridge2(start, adjacency):
    max_length, max_strength = 0, 0
    for nextn in adjacency[start]:
        weight = adjacency[start][nextn]
        if weight == 0:
            continue
        adjacency[start][nextn] = 0
        adjacency[nextn][start] = 0
        length2, strength2 = max_bridge2(nextn, adjacency)
        length = 1 + length2
        strength = weight + strength2
        if length > max_length:
            max_length, max_strength = length, strength
        elif length == max_length:
            max_strength = max(max_strength, strength)
        adjacency[start][nextn] = weight
        adjacency[nextn][start] = weight
    return max_length, max_strength


def code1(adjacency):
    maxi = max_bridge1(0, adjacency)
    return maxi


def code2(adjacency):
    max_length, max_strength = max_bridge2(0, adjacency)
    return max_strength


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
