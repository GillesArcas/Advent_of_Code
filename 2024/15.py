"""
--- Day 15: Warehouse Woes ---
"""


EXAMPLES1 = (
    ('15-exemple1.txt', 2028),
    ('15-exemple2.txt', 10092),
)

EXAMPLES2 = (
    ('15-exemple2.txt', 9021),
)

INPUT = '15.txt'


def read_data(filename):
    with open(filename) as f:
        text = f.readlines()
        return parse_data(text)


def parse_data(text):
    array = []
    moves = ''
    for line in (_.strip() for _ in text):
        if line and line[0] == '#':
            array.append(list(line))
        elif line and line[0] in '<>^v':
            moves += line
    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char == '@':
                i0, j0 = i, j
                break
    return array, moves, i0, j0


def expand_array(array):
    EXPAND = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    newarray = []
    for line in array:
        newline = []
        for x in line:
            newline.extend(list(EXPAND[x]))
        newarray.append(newline)
    return newarray


def applymove(array, i, j, move):
    IDELTA = {'<': 0, '>': 0, '^': -1, 'v': 1}
    JDELTA = {'<': -1, '>': 1, '^': 0, 'v': 0}
    idelta = IDELTA[move]
    jdelta = JDELTA[move]
    i2 = i + idelta
    j2 = j + jdelta
    n = 0
    while array[i2][j2] == 'O':
        i2 = i2 + idelta
        j2 = j2 + jdelta
        n += 1
    if array[i2][j2] == '#':
        return array, i, j
    else:
        for _ in range(n + 1):
            array[i2][j2] = array[i2 - idelta][j2 - jdelta]
            array[i2 - idelta][j2 - jdelta] = '.'
            i2 = i2 - idelta
            j2 = j2 - jdelta
        return array, i2 + idelta, j2 + jdelta


def score(array):
    result = 0
    for i, line in enumerate(array):
        for j, char in enumerate(line):
            if char in 'O[':
                result += 100 * i + j
    return result


def showarray(array):
    for line in array:
        print(''.join(line))
    print()


def code1(data):
    array, moves, i, j = data
    # showarray(array)
    for move in moves:
        array, i, j = applymove(array, i, j, move)
        # showarray(array)
    return score(array)


def movebox(array, ifrom, jfrom, ito, jto):
    assert array[ifrom][jfrom] == '['

    array[ito][jto] = '['
    array[ito][jto + 1] = ']'
    array[ifrom][jfrom] = '.'
    array[ifrom][jfrom + 1] = '.'


def pushupbox(array, i, j):
    """
    Upward. Recursive. Return the set of the pushed boxes.
    """
    assert array[i][j] == '['

    if array[i - 1][j] == '#' or array[i - 1][j + 1] == '#':
        #   #x      x#
        #   []  or  []
        return None
    elif array[i - 1][j] == '.' and array[i - 1][j + 1] == '.':
        #   ..
        #   []
        return {(i, j)}
    elif array[i - 1][j] == '[':
        #   []
        #   []
        if r := pushupbox(array, i - 1, j):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i - 1][j] == ']' and array[i - 1][j + 1] == '.':
        #  [].
        #   []
        if r := pushupbox(array, i - 1, j - 1):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i - 1][j] == '.' and array[i - 1][j + 1] == '[':
        #   .[]
        #   []
        if r := pushupbox(array, i - 1, j + 1):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i - 1][j] == ']' and array[i - 1][j + 1] == '[':
        #  [][]
        #   []
        r1 = pushupbox(array, i - 1, j - 1)
        r2 = pushupbox(array, i - 1, j + 1)
        if r1 and r2:
            return {(i, j)}.union(r1).union(r2)
        else:
            return None
    else:
        assert 0


def pushdnbox(array, i, j):
    """
    Downward. Recursive. Return the set of the pushed boxes.
    """
    assert array[i][j] == '['

    if array[i + 1][j] == '#' or array[i + 1][j + 1] == '#':
        #   []  or  []
        #   #x      x#
        return None
    elif array[i + 1][j] == '.' and array[i + 1][j + 1] == '.':
        #   []
        #   ..
        return {(i, j)}
    elif array[i + 1][j] == '[':
        #   []
        #   []
        if r := pushdnbox(array, i + 1, j):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i + 1][j] == ']' and array[i + 1][j + 1] == '.':
        #   []
        #  [].
        if r := pushdnbox(array, i + 1, j - 1):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i + 1][j] == '.' and array[i + 1][j + 1] == '[':
        #   []
        #   .[]
        if r := pushdnbox(array, i + 1, j + 1):
            return {(i, j)}.union(r)
        else:
            return None
    elif array[i + 1][j] == ']' and array[i + 1][j + 1] == '[':
        #   []
        #  [][]
        r1 = pushdnbox(array, i + 1, j - 1)
        r2 = pushdnbox(array, i + 1, j + 1)
        if r1 and r2:
            return {(i, j)}.union(r1).union(r2)
        else:
            return None
    else:
        assert 0


def pushwestbox(array, i, j):
    assert array[i][j] == ']'

    if array[i][j - 2] == '#':
        return False
    elif array[i][j - 2] == '.':
        array[i][j - 2] = '['
        array[i][j - 1] = ']'
        array[i][j - 0] = '.'
        return True
    elif array[i][j - 2] == ']':
        if pushwestbox(array, i, j - 2):
            array[i][j - 2] = '['
            array[i][j - 1] = ']'
            array[i][j - 0] = '.'
            return True
    else:
        assert 0


def pusheastbox(array, i, j):
    assert array[i][j] == '['

    if array[i][j + 2] == '#':
        return False
    elif array[i][j + 2] == '.':
        array[i][j:j + 3] = '.[]'
        return True
    elif array[i][j + 2] == '[':
        if pusheastbox(array, i, j + 2):
            array[i][j:j + 3] = '.[]'
            return True
    else:
        assert 0


def pushbox(array, i, j, move):
    assert array[i][j] == '@'

    IDELTA = {'<': 0, '>': 0, '^': -1, 'v': 1}
    JDELTA = {'<': -1, '>': 1, '^': 0, 'v': 0}
    idelta = IDELTA[move]
    jdelta = JDELTA[move]
    i2 = i + idelta
    j2 = j + jdelta
    if array[i2][j2] == '#':
        return i, j
    if array[i2][j2] == '.':
        array[i][j] = '.'
        array[i2][j2] = '@'
        return i2, j2

    if move == '^':
        if array[i - 1][j] == '[':
            r = pushupbox(array, i - 1, j)
        elif array[i - 1][j] == ']':
            r = pushupbox(array, i - 1, j - 1)
        else:
            assert 0
        if r:
            for ii, jj in sorted(r):
                movebox(array, ii, jj, ii - 1, jj)
            array[i][j] = '.'
            i -= 1
    elif move == 'v':
        if array[i + 1][j] == '[':
            r = pushdnbox(array, i + 1, j)
        elif array[i + 1][j] == ']':
            r = pushdnbox(array, i + 1, j - 1)
        else:
            assert 0
        if r:
            for ii, jj in sorted(r, reverse=True):
                movebox(array, ii, jj, ii + 1, jj)
            array[i][j] = '.'
            i += 1
    elif move == '<':
        assert array[i][j - 1] == ']'
        if pushwestbox(array, i, j - 1):
            array[i][j] = '.'
            j -= 1
    elif move == '>':
        assert array[i][j + 1] == '['
        if pusheastbox(array, i, j + 1):
            array[i][j] = '.'
            j += 1

    array[i][j] = '@'
    return i, j


def code2(data):
    array, moves, i, j = data
    array = expand_array(array)
    j *= 2
    # showarray(array)
    for move in moves:
        i,j = pushbox(array, i, j, move)
        # showarray(array)
    return score(array)


def test(n, code, examples, myinput):
    for fn, expected in examples:
        data = read_data(fn)
        result = code(data)
        assert expected is None or result == expected, (data, expected, result)

    print(f'{n}>', code(read_data(myinput)))


test(1, code1, EXAMPLES1, INPUT)
test(2, code2, EXAMPLES2, INPUT)
