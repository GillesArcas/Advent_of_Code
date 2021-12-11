
EXAMPLES1 = (
    ('11-exemple1.txt', 1656),
)

EXAMPLES2 = (
    ('11-exemple1.txt', 195),
)

INPUT =  '11.txt'


def read_data(fn):
    data = list()
    with open(fn) as f:
        for line in f:
            line = line.strip()
            data.append([int(_) for _ in line])
    return data


def neighbours(data, i, j):
    neigh = list()
    for i2 in range(i - 1, i + 2):
        for j2 in range(j - 1, j + 2):
            neigh.append((i2, j2))
    return [(i2, j2) for i2, j2 in neigh if (i2, j2) != (i, j) and 0 <= i2 < len(data) and 0 <= j2 < len(data[0])]


def display(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            print('%3d' % data[i][j], end='')
        print()


def step(data):
    flashes = set()
    for i in range(len(data)):
        for j in range(len(data[0])):
            data[i][j] += 1

    while True:
        nb_flash = 0
        for i in range(len(data)):
            for j in range(len(data[0])):
                if data[i][j] > 9 and (i, j) not in flashes:
                    nb_flash += 1
                    flashes.add((i, j))
                    for (i2, j2) in neighbours(data, i, j):
                        data[i2][j2] += 1
        if nb_flash == 0:
            break

    for (i, j) in flashes:
        data[i][j] = 0

    return len(flashes)


def code1(data):
    nb_flashes = 0
    for nb_step in range(1, 101):
        nb_flashes += step(data)
    return nb_flashes


def code2(data):
    for nb_step in range(1, 100000):
        nb_flashes = step(data)
        if nb_flashes == len(data) * len(data):
            return nb_step


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
