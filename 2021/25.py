
EXAMPLES1 = (
    ('25-exemple1.txt', 58),
)

EXAMPLES2 = (
)

INPUT = '25.txt'


def read_data(fn):
    with open(fn) as f:
        lines = [line.strip() for line in f.readlines()]
    array = [list(line) for line in lines]
    return array


def print_data(array):
    for line in array:
        print(''.join(line))


def iterstep(array):
    change = False

    moves = list()
    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char == '>':
                j2 = (j + 1) % len(line)
                if array[i][j2] == '.':
                    moves.append((i, j, j2))
    for i, j, j2 in moves:
        array[i][j] = '.'
        array[i][j2] = '>'
        change = True

    moves = list()
    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char == 'v':
                i2 = (i + 1) % len(array)
                if array[i2][j] == '.':
                    moves.append((i, i2, j))
    for i, i2, j in moves:
        array[i][j] = '.'
        array[i2][j] = 'v'
        change = True

    return array, change


def code1(array):
    print_data(array)
    print()
    change = True
    n = 0
    while change:
        array, change = iterstep(array)
        n += 1
    print(n)
    print_data(array)
    return n


def code2(array):
    return None


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
# test(2, code2, EXAMPLES2, INPUT)
